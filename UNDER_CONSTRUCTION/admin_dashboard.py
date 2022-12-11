import tkinter as tk

win = tk.Tk()
win.config(padx=10, pady=10)
win.title("Admin Panel")
win.geometry("1000x800")

image = tk.Button(text="IMAGE")
image.grid(row=0, column=0, padx=40)

control = tk.Frame(win, width=810, height=50, bg='cyan')
control.grid(row=0, column=1, pady=10, padx=10)

data_panel = tk.Frame(win, width=940, height=690, bg='grey')
data_panel.grid(row=1, column=0, columnspan=2)

win.mainloop()