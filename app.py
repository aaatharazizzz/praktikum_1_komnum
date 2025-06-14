import math
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
    def __init__(self, xl, xr, f_xl, f_xr, xm, f_xm):
        self.xl = xl
        self.xr = xr
        self.f_xl = f_xl
        self.f_xr = f_xr
        self.xm = xm
        self.f_xm = f_xm

def get_regula_falsi(x1, x2, x_lambda):
    f_x1 = x_lambda(x1)
    f_x2 = x_lambda(x2)
    return (x2 - ((f_x2 * (x1 - x2))/(f_x1 - f_x2)))

class Simulation:
    def __init__(self):
        self.precision=6
        self.simulation_started=False
        self.formula_str=""
        self.x_lambda = lambda x: None
        self.simulation_result : list[RegulaFalsiResult] = []
        px = 1/ mpl.rcParams['figure.dpi']
        self.fig, self.ax = mpl.subplots(figsize=(600*px, 400*px))
        self.fig.patch.set_facecolor("#FFFFFF")
    def refresh_figure(self, iter_no : int):
        if(iter_no > len(self.simulation_result) or iter_no < 1):
            tkinter.messagebox.showerror("Error", message="Cannot refresh figure: Iter No. too small or too big")
            return
        result = self.simulation_result[iter_no-1]
        pad = abs((result.xr - result.xl))
        x_vals = numpy.linspace(result.xl-pad, result.xr+pad, 400)
        y_vals = self.x_lambda(x_vals)
        
        self.ax.clear()
        self.ax.set_xlim(result.xl-pad, result.xr+pad)
        self.ax.set_title(f"[Iteration {iter_no}]   f(x)={self.formula_str} ")
        self.ax.axvline(x=0, color='black', linewidth=0.5, aa=False)
        self.ax.axhline(y=0, color='black', linewidth=0.5, aa=False)
        self.ax.plot(x_vals, y_vals)
        self.ax.plot([result.xl, result.xl], [result.f_xl, 0], color='g', linestyle=':', linewidth=2)
        self.ax.plot([result.xr, result.xr], [result.f_xr, 0], color='r', linestyle=':', linewidth=2)
        self.ax.plot([result.xl, result.xr], [result.f_xl, result.f_xr], color='y')
        self.ax.plot(result.xl, result.f_xl, color='g', marker="s", label="xl")
        self.ax.plot(result.xr, result.f_xr, color='r', marker="s", label="xr")
        self.ax.plot(result.xm, 0, color='y', marker="s", label="xm")
        self.ax.legend(loc="upper left")
        self.fig.canvas.draw()
    def push_result(self, result, treeview):
        self.simulation_result.append(RegulaFalsiResult(
            result.xl, result.xr, result.f_xl, result.f_xr, result.xm, result.f_xm
        )) 
        treeview.insert(parent='', index='end', iid=len(self.simulation_result)-1, values=(
            len(self.simulation_result), result.xl, result.xr, result.f_xl, result.f_xr, result.xm, result.f_xm
        ))
        treeview.update()
    def iterate(self, treeview):
        if self.simulation_started == False:
            tkinter.messagebox.showerror("Error", message="Initialize simulation before iterating")
            return
        old_len = len(self.simulation_result)
        last_result = self.simulation_result[old_len-1]
        if(last_result.f_xm == 0.0):
            tkinter.messagebox.showinfo("Info", message="No longer iterating: f(xm) is already 0")
            return
        new_xl = last_result.xl
        new_xr = last_result.xr
        if(math.copysign(1, last_result.f_xm) == math.copysign(1, last_result.f_xr)):
            new_xr = last_result.xm
        else:
            new_xl = last_result.xm
        try:
            new_f_xl = round(self.x_lambda(new_xl), self.precision)
            new_f_xr = round(self.x_lambda(new_xr), self.precision)
            new_xm = round(get_regula_falsi(new_xl, new_xr, x_lambda=self.x_lambda), self.precision)
            new_f_xm = round(self.x_lambda(new_xm), self.precision)
        except ZeroDivisionError:
            tkinter.messagebox.showerror("Error", message="Cannot push iteration: Zero division error")
            return
        result = RegulaFalsiResult(new_xl, new_xr, new_f_xl, new_f_xr, new_xm, new_f_xm) 
        self.push_result(result, treeview)
        self.refresh_figure(len(self.simulation_result))
    def start(self, formula_str, x1, x2, precision, treeview):
        self.simulation_started = False
        try:
            formula = sympy_parser.parse_expr(formula_str, transformations='all')
        except:
            tkinter.messagebox.showerror("Error", message="f(x) cannot be parsed")
            return
        for s in formula.free_symbols:
                if s != sympy.Symbol('x'):
                    tkinter.messagebox.showerror("Error", message="f(x) contains a variable that is not \"x\"")
                    return
        self.x_lambda = sympy.lambdify(sympy.symbols('x'), formula, modules=['numpy'])
        x1 = round(x1, precision)
        x2 = round(x2, precision)
        try:
            f_x1 = round(self.x_lambda(x1), precision)
            f_x2 = round(self.x_lambda(x2), precision)
            if(math.copysign(1.0, f_x1) == math.copysign(1.0, f_x2)):
                tkinter.messagebox.showwarning("Warning", message=f"Regula falsi method may not work: f(xl) and f(xr) has the same sign! (f(xl)={f_x1}, f(xr)={f_x2})")
            x3 = round(get_regula_falsi(x1, x2, x_lambda=self.x_lambda), precision)
            f_x3 = round(self.x_lambda(x3), precision)
        except ZeroDivisionError:
            tkinter.messagebox.showerror("Error", message="Cannot push first iteration: Zero division error")
            return
        self.simulation_result.clear()
        for i in treeview.get_children():
            treeview.delete(i)
        init_result = RegulaFalsiResult(x1, x2, f_x1, f_x2, x3, f_x3) 
        self.push_result(init_result, treeview)
        self.precision = precision
        self.formula_str = formula_str
        self.refresh_figure(1)
        self.simulation_started = True
regula_falsi_sim = Simulation()

window = tkinter.Tk()
window.title("Program Praktikum 1 Komnum 6")
window.geometry('1000x800')

upper_frame = tkinter.Frame(window)
upper_frame.grid(row=0, column=0)
lower_frame = tkinter.Frame(window)
lower_frame.grid(row=1, column=0)

upper_left_frame = tkinter.Frame(upper_frame, padx=20, pady=20)
upper_left_frame.grid(row=0, column=0)

upper_right_frame = tkinter.Frame(upper_frame)
upper_right_frame.grid(row=0, column=1)

user_input_frame = tkinter.LabelFrame(upper_left_frame, text="Setup", padx=20, pady=20)
user_input_frame.grid(row=0, column=0, sticky="nsew")

iter_control_frame = tkinter.LabelFrame(upper_left_frame, text="Iteration Control", padx=20, pady=20)
iter_control_frame.grid(row=1, column=0, sticky="nsew")

output_table_frame = tkinter.LabelFrame(lower_frame, text="Output", padx=20, pady=20)
output_table_frame.grid(row=0, column=0)
output_table_treeview = ttk.Treeview(output_table_frame)
output_table_treeview.grid(row=0, column=0)

canvas_frame = tkinter.LabelFrame(upper_right_frame, text="Graph", padx=20, pady=20)
canvas_frame.grid(row=0, column=0)

formula_input_label = tkinter.Label(user_input_frame, text="Enter f(x) function")
formula_input_entry = tkinter.Entry(user_input_frame)
start_variable_frame = tkinter.LabelFrame(user_input_frame, text="Start values")
start_x1_label = tkinter.Label(start_variable_frame, text="x1")
start_x1_entry = tkinter.Entry(start_variable_frame, width=15)
start_x2_label = tkinter.Label(start_variable_frame, text="x2")
start_x2_entry = tkinter.Entry(start_variable_frame, width=15)
round_label = tkinter.Label(user_input_frame, text="Precision")
round_entry = tkinter.Entry(user_input_frame)
round_entry.insert(tkinter.END, "6")

output_table_treeview['columns'] = ("No.", "xl", "xr", "f(xl)", "f(xr)", "xm", "f(xm)")
output_table_treeview.column("#0", width=0, stretch='NO')
output_table_treeview.column("No.", width=48)
output_table_treeview.column("xl", width=100)
output_table_treeview.column("xr", width=100)
output_table_treeview.column("f(xl)", width=100)
output_table_treeview.column("f(xr)", width=100)
output_table_treeview.column("xm", width=100)
output_table_treeview.column("f(xm)", width=100)
output_table_treeview.heading("#0", text="", anchor='w')
output_table_treeview.heading("No.", text="No.", anchor='w')
output_table_treeview.heading("xl", text="xl", anchor='w')
output_table_treeview.heading("xr", text="xr", anchor='w')
output_table_treeview.heading("f(xl)", text="f(xl)", anchor='w')
output_table_treeview.heading("f(xr)", text="f(xr)", anchor='w')
output_table_treeview.heading("xm", text="xm", anchor='w')
output_table_treeview.heading("f(xm)", text="f(xm)", anchor='w')

fig_canvas = FigureCanvasTkAgg(regula_falsi_sim.fig, master=canvas_frame)
fig_canvas.get_tk_widget().grid(row=0, column=0)
graph_toolbar = NavigationToolbar2Tk(fig_canvas, canvas_frame, pack_toolbar=False)
graph_toolbar.grid(row=1, column=0)
graph_toolbar.update()

def on_start(sim : Simulation, formula_str, x1_str, x2_str, precision_str, treeview):
    try:
        x1 = float(x1_str)
        x2 = float(x2_str)
    except ValueError:
        tkinter.messagebox.showerror("Error", message="Cannot convert x1 or x2 to float")
        return
    try:
        precision = int(precision_str)
    except ValueError:
        tkinter.messagebox.showerror("Error", message="Cannot convert precision to int")
        return
    sim.start(formula_str, x1, x2, precision, treeview)
def on_iter_view(sim : Simulation, iter_no_str):
    try:
        iter_no = int(iter_no_str)
    except ValueError:
        tkinter.messagebox.showerror("Error", message="Cannot convert iter no. to int")
        return
    sim.refresh_figure(iter_no)

start_button = tkinter.Button(user_input_frame, 
    text="Start", 
    command=lambda: on_start(
        sim=regula_falsi_sim,
        formula_str=formula_input_entry.get(),
        x1_str=start_x1_entry.get(),
        x2_str=start_x2_entry.get(),
        precision_str=round_entry.get(),
        treeview=output_table_treeview
    )
)
iter_button = tkinter.Button(iter_control_frame, 
    text="Push New Iteration", 
    command=lambda: regula_falsi_sim.iterate(output_table_treeview), 
    anchor='c'
)

show_iter_label = tkinter.Label(iter_control_frame, text="View iteration no.", anchor='c')
show_iter_entry = tkinter.Entry(iter_control_frame, width=4)
show_iter_button = tkinter.Button(iter_control_frame, text="View", command=lambda: on_iter_view(regula_falsi_sim, show_iter_entry.get()))

formula_input_label.grid(row=0, column=0)
formula_input_entry.grid(row=1, column=0)
start_variable_frame.grid(row=2, column=0)
start_x1_label.grid(row=0, column=0)
start_x1_entry.grid(row=1, column=0)
start_x2_label.grid(row=0, column=1)
start_x2_entry.grid(row=1, column=1)
round_label.grid(row=3, column=0)
round_entry.grid(row=4, column=0)
start_button.grid(row=5, column=0, padx=5, pady=5)
iter_button.grid(row=0, column=0, padx=5, pady=5, columnspan=3)
show_iter_label.grid(row=1, column=0)
show_iter_entry.grid(row=1, column=1, padx=5, pady=5)
show_iter_button.grid(row=1, column=2, padx=5, pady=5)


window.mainloop()