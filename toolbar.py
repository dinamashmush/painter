import tkinter as tk
from tkinter import colorchooser
from typing import *
from dropdown import DropDown
from PIL import Image, ImageTk

from inspect import signature
class ToolBar(tk.Frame):
    def __init__(self, root, color: tk.StringVar, state: tk.StringVar):
        super().__init__(root)
        self.root = root
        self.pack()
        self.color = color
        self.create_widgets()

    def create_widgets(self) -> None:

        data = bytes.fromhex(" ".join([self.color.get()[1:]]*(16*16)))
        img = Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
        self.color_img = ImageTk.PhotoImage(img)
        self.color_btn: tk.Button = tk.Button(self.root, text = "Color", image=self.color_img, compound="left",
                   command = self.update_color)
        self.color_btn.pack()
        
        
        select_icon_image = Image.open("./assets/3793488.png")
        resize_select_icon = select_icon_image.resize((16, 16))
        self.select_icon = ImageTk.PhotoImage(resize_select_icon)
        self.select_button = tk.Button(self, text="Select", image=self.select_icon, compound="left")
        self.select_button.pack()
        

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

