import numpy as np
import tkinter as tk
from tkinter import messagebox
from math import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Trapezoidal method
def trapezoidal(f, a, b, n):
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h

# Romberg integration
def romberg_integration(f, a, b, max_level):
    R = [[0 for _ in range(max_level)] for _ in range(max_level)]
    for i in range(max_level):
        n = 2**i
        R[i][0] = trapezoidal(f, a, b, n)
        for k in range(1, i + 1):
            R[i][k] = (4*k * R[i][k-1] - R[i-1][k-1]) / (4*k - 1)
    return R

# Fungsi untuk tombol "Hitung"
def hitung():
    try:
        fungsi_str = entry_fungsi.get()
        a = float(entry_a.get())
        b = float(entry_b.get())
        level = int(entry_level.get())

        f = lambda x: eval(fungsi_str)

        R = romberg_integration(f, a, b, level)

        # Tampilkan tabel di Text Widget
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, "Tabel Romberg:\n")
        for i in range(level):
            baris = "\t".join(f"{R[i][j]:.10f}" for j in range(i+1))
            output_text.insert(tk.END, baris + "\n")

        # Tampilkan plot di canvas
        diagonal = [R[i][i] for i in range(level)]
        ax.clear()
        ax.plot(range(1, level+1), diagonal, marker='o', label='R[i][i]')
        ax.axhline(y=2.0, color='red', linestyle='--', label='Eksak (jika ∫sin(x) dx)')
        ax.set_title("Konvergensi Metode Romberg")
        ax.set_xlabel("Level Romberg")
        ax.set_ylabel("Estimasi Integral")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"Ada kesalahan input:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Romberg Integration GUI")

# Input fields
tk.Label(root, text="Fungsi f(x):").grid(row=0, column=0, sticky='e')
entry_fungsi = tk.Entry(root, width=30)
entry_fungsi.insert(0, "sin(x)")
entry_fungsi.grid(row=0, column=1)

tk.Label(root, text="Batas bawah a:").grid(row=1, column=0, sticky='e')
entry_a = tk.Entry(root)
entry_a.insert(0, "0")
entry_a.grid(row=1, column=1)

tk.Label(root, text="Batas atas b:").grid(row=2, column=0, sticky='e')
entry_b = tk.Entry(root)
entry_b.insert(0, "3.1416")
entry_b.grid(row=2, column=1)

tk.Label(root, text="Level Romberg:").grid(row=3, column=0, sticky='e')
entry_level = tk.Entry(root)
entry_level.insert(0, "5")
entry_level.grid(row=3, column=1)

# Tombol Hitung
tk.Button(root, text="Hitung Integrasi", command=hitung).grid(row=4, column=0, columnspan=2, pady=10)

# Output Textbox
output_text = tk.Text(root, height=10, width=60)
output_text.grid(row=5, column=0, columnspan=2)

# Matplotlib Plot Area
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)

root.mainloop()
