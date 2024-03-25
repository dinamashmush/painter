import tkinter as tk
from tkinter import colorchooser
from typing import *
from PIL import Image, ImageTk
from enums import State

class ToolBar(tk.Frame):
    def __init__(self, root, color: tk.StringVar, state: tk.StringVar, width: tk.IntVar):
        super().__init__(root)
        self.root = root
        self.pack()
        self.color = color
        self.state = state
        self.width = width
        self.create_widgets()

    def create_widgets(self) -> None:

        data = bytes.fromhex(" ".join([self.color.get()[1:]]*(16*16)))
        img = Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
        self.color_img = ImageTk.PhotoImage(img)
        self.color_btn: tk.Button = tk.Button(self.root, text = "Color", image=self.color_img, compound="left",
                   command = self.update_color)
        self.color_btn.pack()
        
        def change_selected_state(state: str):
            if self.state.get() == state: 
                self.state.set(State.PAINT.value)
                self.select_button.config(relief="raised")
            else:
                self.state.set(state)
                self.select_button.config(relief="sunken")
        
        
        
        select_icon_image = Image.open("./assets/3793488.png")
        resize_select_icon = select_icon_image.resize((16, 16))
        self.select_icon = ImageTk.PhotoImage(resize_select_icon)
        self.select_button = tk.Button(self, text="Select", image=self.select_icon, compound="left", command=lambda: change_selected_state(State.SELECT.value))
        self.select_button.pack()
        
        validatecommand = (self.register(self.validate_num))
        self.width_input = tk.Spinbox(self, textvariable=self.width, from_=1, to=9, increment=1, validatecommand=(validatecommand,'%P'), validate="all") 
        self.width_input.pack()
        
        # self.erase_btn = tk.Button(self, text="Erase", command=lambda: change_selected_state(State.ERASE.value))
        # self.erase_btn.pack()
    
    def create_widgets_selected(self):
        self.delete_btn = tk.Button(self, text="DELETE", command=self.delete_selected)
        self.delete_btn.pack()


    def validate_num(self, P):
        if len(P)>1:
            return False
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

        

    def update_color(self) -> None:
        color = colorchooser.askcolor(title ="Choose color")[1]
        if not color: return #!error message
        self.color.set(color)
        data = bytes.fromhex(" ".join([color[1:]]*(16*16)))
        img = Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
        self.color_img = ImageTk.PhotoImage(img)
        self.color_btn.config(image=self.color_img)

    def say_hi(self):
        print("hi there, everyone!")