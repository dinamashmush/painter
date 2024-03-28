import tkinter as tk

from typing import *
from components.color_btn import ColorBtn
from helper_funcs.validate_funcs import validate_width

class ShapeOptions(tk.Toplevel):
    def __init__(self, master, fill: str, color: str, width: int, on_save:Callable, multiple:bool):
        super().__init__(master)
        self.geometry("500x250+150+150")
        self.grab_set()


        self.fill = fill
        self.color = color
        self.width = width
        self.on_save = on_save
        self.multiple = multiple
        
        self.create_widgets()
        
    def create_widgets(self) -> None:
        
        if self.multiple:
            self.warning_label = tk.Label(self, text="Please note that these changes will affect all selected shapes and freestyle strokes.")
            self.warning_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        
        def set_color(color:str) -> None:
            self.color = color
        def set_fill(color:str) -> None:
            self.fill = color

        self.color_btn = ColorBtn(self, text = "Color", color=self.color, on_change=set_color)
        self.color_btn.grid(row = 1, column=0, pady=10, padx=(10, 0))
        
        self.fill_frame = tk.Frame(self)
        
        self.fill_btn = ColorBtn(self.fill_frame, text = "Fill", color=self.fill, on_change=set_fill)
        def no_fill_command() -> None:
            self.fill = ""
            self.fill_btn.configure(image="")
        
        self.no_fill_btn: tk.Button = tk.Button(self.fill_frame, text="no fill", command=no_fill_command)

        self.fill_frame.grid(column=1, row=1, padx=(10, 10), pady=10)
        
        self.fill_btn.pack(side=tk.LEFT, padx=6)
        self.no_fill_btn.pack(side=tk.LEFT)
        
        
        self.width_label = tk.Label(self, text="Width: ")
        self.width_label.grid(row=1, column=2, pady=10)
        
        validatecommand = (self.register(validate_width))
        self.width_spinbox = tk.Spinbox(self, from_=1, to=9, validatecommand=(validatecommand,'%P'), validate="all")
        
        self.width_spinbox.delete(0, "end")
        self.width_spinbox.insert(0, str(self.width))
        self.width_spinbox.grid(column=3, row=1, pady=10)
        
        self.btns_frame = tk.Frame(self)
        self.btns_frame.grid(column=4, row=2, padx=(5, 0), pady=(150, 0))
        
        self.save_btn = tk.Button(self.btns_frame, command=self.save_changes, text="save")
        self.cancel_btn = tk.Button(self.btns_frame, command=self.destroy, text="cancel")
        self.save_btn.pack(side=tk.LEFT)
        self.cancel_btn.pack(padx=5, side=tk.LEFT)


    def save_changes(self) -> None:
        if not len(self.width_spinbox.get()):
            self.warning = tk.Label(self, text="Please Enter a Valid Width", fg="red")
            self.warning.grid(row=2, column=0, columnspan=4)
            return
        self.on_save(fill=self.fill, color=self.color, width=int(self.width_spinbox.get()))
        self.destroy()
        