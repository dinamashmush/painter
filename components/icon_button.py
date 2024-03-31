import tkinter as tk
from PIL import Image, ImageTk

from typing import *

class IconButton(tk.Button):
    """a button with an icon"""
    def __init__(self, master, img_path:str, img_size:int,   command:Callable,text:str="", btn_size:int=0) -> None:
        icon_image = Image.open(img_path)
        resize_icon = icon_image.resize((img_size, img_size))
        self.icon = ImageTk.PhotoImage(resize_icon)
        if btn_size:
            super().__init__(master, compound="left" , image=self.icon, width=btn_size, height=btn_size, text=text, command=command)
        else:
            super().__init__(master, compound="left" , image=self.icon, text=text, command=command)
            