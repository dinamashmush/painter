import tkinter as tk
from tkinter import colorchooser
from typing import *
from PIL import Image, ImageTk
from validate_funcs import validate_width

class ShapeOptions(tk.Toplevel):
    def __init__(self, master, fill: str, color: str, width: int, on_save:Callable):
        super().__init__(master)
        self.geometry("500x250+150+150")

        self.fill = fill
        self.color = color
        self.width = width
        self.on_save = on_save
        self.create_widgets()
        
    def create_widgets(self) -> None:
        
        data = bytes.fromhex(" ".join([self.color[1:]]*(16*16)))
        img = Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
        self.color_img = ImageTk.PhotoImage(img)
        self.color_btn: tk.Button = tk.Button(self, text = "Color", image=self.color_img, compound="left",
                   command = self.update_color)
        self.color_btn.grid(column=0, row=0)
        
        
        self.fill_btn: tk.Button = tk.Button(self, text = "Fill", compound="left",
                   command = self.update_fill)
        self.fill_btn.grid(column=1, row=0)
        
        
        self.width_label = tk.Label(self, text="Width")
        self.width_label.grid(row=0, column=2)
        
        validatecommand = (self.register(validate_width))
        self.width_spinbox = tk.Spinbox(self, from_=1, to=9, validatecommand=(validatecommand,'%P'), validate="all")
        
        self.width_spinbox.delete(0, "end")
        self.width_spinbox.insert(0, str(self.width))
        self.width_spinbox.grid(column=3, row=0)
        
        self.btns_frame = tk.Frame(self)
        self.btns_frame.grid(column=4, row=2, padx=(5, 0), pady=(50, 0))
        
        self.save_btn = tk.Button(self.btns_frame, command=self.save_changes, text="save")
        self.cancel_btn = tk.Button(self.btns_frame, command=self.destroy, text="cancel")
        self.save_btn.pack(side=tk.LEFT)
        self.cancel_btn.pack(padx=5, side=tk.LEFT)


    def update_color(self) -> None:
        picked_color = self.pick_color()
        if not picked_color:
            return
        color, img = picked_color
        self.color = color
        self.color_img = ImageTk.PhotoImage(img)
        self.color_btn.config(image=self.color_img)
        
    def update_fill(self, delete: bool=False) -> None:
        if delete:
            color = ""
            self.fill_btn.config(image="")
        else:
            picked_color = self.pick_color()
            if not picked_color:
                return
            color, img = picked_color
            self.fill_img = ImageTk.PhotoImage(img)
            self.fill_btn.config(image=self.fill_img)
        self.fill = color

    def pick_color(self) -> Union[Literal[None], Tuple[str, Image.Image]]:
        color = colorchooser.askcolor(parent=self, title ="Choose color")[1]
        if not color: return None
        data = bytes.fromhex(" ".join([color[1:]]*(16*16)))
        return color, Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)

    def save_changes(self) -> None:
        self.on_save(fill=self.fill, color=self.color, width=int(self.width_spinbox.get()))
        self.destroy()
        