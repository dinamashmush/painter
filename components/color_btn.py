import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageTk
from typing import *


class ColorBtn(tk.Button):
    """a button with a small image of the picked color to pick a color
    """
    def __init__(self, master: tk.Misc, text:str, color:str, on_change:Callable[[str], None]) -> None:
        super().__init__(master, text=text, compound="left", command=self.btn_command)
        self.color = color
        self.get_image()
        self.configure(image=self.color_img)
        self.on_change = on_change
        
    def btn_command(self) -> None:
        pick = self.pick_color()
        if pick:
            color, img = pick
            self.color_img: Union[ImageTk.PhotoImage, str] = ImageTk.PhotoImage(img)
            self.configure(image=self.color_img)
            self.on_change(color)
            
    def get_image(self) -> None:
        if not  len(self.color):
            self.color_img = ""
            return
        data = bytes.fromhex(" ".join([self.color[1:]]*(16*16)))
        img = Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
        self.color_img = ImageTk.PhotoImage(img)
    
    def pick_color(self) -> Union[Literal[None], Tuple[str, Image.Image]]:
        color = colorchooser.askcolor(parent=self, title ="Choose color")[1]
        if not color: return None
        data = bytes.fromhex(" ".join([color[1:]]*(16*16)))
        return color, Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
