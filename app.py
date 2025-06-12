import tkinter
from tkinter import ttk
import matplotlib.pyplot as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy
import sympy
import sympy.parsing.sympy_parser as sympy_parser
from sympy.printing import latex

class RegulaFalsiResult:
    def __init__(self, x_no, x, fx):
        self.x_no = x_no
        self.x = x
        self.fx = fx

class Simulation:
    def __init__(self):
        simulation_started=False
        simulation_formula_str = ""
        simulation_result = 10
        fig, ax = mpl.subplots()
        fig.patch.set_facecolor("#FFFFFF")
    def iterate(self):
        pass
"""

simulation_started = False
simulation_formula_str = ""
simulation_result = []
fig, ax = mpl.subplots()
fig.patch.set_facecolor("#FFFFFF")

def push_regula_falsi_result(result_array) :
    global simulation_formula_str
    print(simulation_formula_str)
    formula = sympy_parser.parse_expr(simulation_formula_str, transformations='all')
    x_lambda = sympy.lambdify(sympy.symbols('x'), formula, modules=['numpy'])
    result_len = len(result_array)
    curr_x1 = result_array[result_len-2].x
    curr_x2 = result_array[result_len-1].x
    curr_fx1 = result_array[result_len-2].fx
    curr_fx2 = result_array[result_len-1].fx
    curr_x3 = curr_x2 - ((curr_fx2 * (curr_x1 - curr_x2)) / (curr_fx1 - curr_fx2))
    curr_fx3 = x_lambda(curr_x3)
    result_array.append(RegulaFalsiResult(result_len + 1, curr_x3, curr_fx3))

def start_simulation(formula_str : str, x1_str, x2_str, treeview):
    global simulation_formula_str, simulation_started
    try:
        simulation_formula_str = formula_str
        formula = sympy_parser.parse_expr(simulation_formula_str, transformations='all')
    except:
        tkinter.messagebox.showerror("Error", message="f(x) cannot be parsed")
        return
    for s in formula.free_symbols:
            if s != sympy.Symbol('x'):
                tkinter.messagebox.showerror("Error", message="f(x) contains a variable that is not \"x\"")
                return
    x_lambda = sympy.lambdify(sympy.symbols('x'), formula, modules=['numpy'])
    print(simulation_formula_str)
    try:
        x1 = float(x1_str)
        x2 = float(x2_str)
    except ValueError:
        tkinter.messagebox.showerror("Error", message="Cannot convert to float")
        return
    simulation_result.clear()
    simulation_result.append(RegulaFalsiResult(1, x1, x_lambda(x1)))
    simulation_result.append(RegulaFalsiResult(2, x2, x_lambda(x2)))
    push_regula_falsi_result(simulation_result)
    for i in treeview.get_children():
        treeview.delete(i)
    for i, result in enumerate(simulation_result):
        treeview.insert(parent='', index='end', iid=i, values=(result.x_no, result.x, result.fx))
    treeview.update()
    refresh_figure(x1, x2, simulation_result[2].x)
    simulation_started = True
    

def iterate(treeview):
    if simulation_started == False:
        tkinter.messagebox.showerror("Error", message="Initialize simulation before iterating")
        return
    push_regula_falsi_result(simulation_result)
    result_len = len(simulation_result)
    treeview.insert(parent='', index='end', iid=result_len-1, values=(simulation_result[result_len-1].x_no, simulation_result[result_len-1].x, simulation_result[result_len-1].fx))
    treeview.update()
    refresh_figure(simulation_result[result_len-3].x, simulation_result[result_len-2].x, simulation_result[result_len-1].x)

def refresh_figure(x1, x2, x3):
    global simulation_formula_str
    formula = sympy_parser.parse_expr(simulation_formula_str, transformations='all')
    x_lambda = sympy.lambdify(sympy.symbols('x'), formula, modules=['numpy'])
    x_vals = numpy.linspace(x1-3, x2+3, 400)
    y_vals = x_lambda(x_vals)
    
    ax.clear()
    ax.set_xlim(x1-3, x2+3)
    ax.set_title("Hello")
    ax.axvline(x=0, color='black', linewidth=0.5, aa=False)
    ax.axhline(y=0, color='black', linewidth=0.5, aa=False)
    ax.plot(x_vals, y_vals)
    ax.axvline(x=x1, color='g', linestyle=':')
    ax.axvline(x=x2, color='r', linestyle=':')
    ax.plot(x3, 0, color='y', marker="s", label="x3")
    ax.legend(loc="upper left")
"""
window = tkinter.Tk()
window.title("Program Praktikum 1 Komnum 6")
window.geometry('800x400')

frame = tkinter.Frame(window)
frame.pack()

user_input_frame = tkinter.LabelFrame(frame, text="Setup", padx=20, pady=20)
formula_input_label = tkinter.Label(user_input_frame, text="Masukkan fungsi f(x)")
formula_input_entry = tkinter.Entry(user_input_frame)
start_variable_frame = tkinter.LabelFrame(user_input_frame, text="Nilai awal")
start_x1_label = tkinter.Label(start_variable_frame, text="x1")
start_x1_entry = tkinter.Entry(start_variable_frame)
start_x2_label = tkinter.Label(start_variable_frame, text="x2")
start_x2_entry = tkinter.Entry(start_variable_frame)

output_table_frame = tkinter.LabelFrame(frame, text="Output", padx=20, pady=20)
output_table_treeview = ttk.Treeview(output_table_frame)

output_table_treeview['columns'] = ("i", "xi", "f(xi)")
output_table_treeview.column("#0", width=0, stretch='NO')
output_table_treeview.column("i")
output_table_treeview.column("xi")
output_table_treeview.column("f(xi)")
output_table_treeview.heading("#0", text="", anchor='w')
output_table_treeview.heading("i", text="i", anchor='w')
output_table_treeview.heading("xi", text="xi", anchor='w')
output_table_treeview.heading("f(xi)", text="f(xi)", anchor='w')
canvas_frame = tkinter.LabelFrame(frame, text="Graph", padx=20, pady=20)

start_button = tkinter.Button(user_input_frame, text="Run")
iter_button = tkinter.Button(user_input_frame, text="Iterate")

fig_canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
graph_toolbar = NavigationToolbar2Tk(fig_canvas, canvas_frame)
graph_toolbar.update()

user_input_frame.grid(row=0, column=0)
formula_input_label.pack()
formula_input_entry.pack()
start_variable_frame.pack()
start_x1_label.grid(row=0, column=0)
start_x1_entry.grid(row=1, column=0)
start_x2_label.grid(row=0, column=1)
start_x2_entry.grid(row=1, column=1)
start_button.pack()
iter_button.pack()
canvas_frame.grid(row=0, column=1)
fig_canvas.get_tk_widget().pack()
output_table_frame.grid(row=0, column=2)
output_table_treeview.pack()

window.mainloop()