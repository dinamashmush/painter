import tkinter as tk
from toolbar import ToolBar
from math import *
from typing import *
from painter import Painter
from enums import State

from export_funcs import *


class Application(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0)
        self.color = tk.StringVar(self, "#ffffff")
        self.fill = tk.StringVar(self, "")
        self.state = tk.StringVar(self, State.PAINT.value)
        self.width = tk.IntVar(self, 3)
        self.font = tk.StringVar(self, "Arial")
        self.font_size = tk.IntVar(self, 14)

        self.create_widgets()

    def create_widgets(self) -> None:
        self.painter = Painter(
            self,
            root=self.master,
            color=self.color,
            fill=self.fill,
            state=self.state,
            font=self.font,
            font_size=self.font_size,
            width=self.width)

        self.toolbar = ToolBar(
            self, 
            color=self.color, 
            fill=self.fill,
            state=self.state, 
            font=self.font,
            font_size=self.font_size,
            width=self.width, 
            export={
            "png": lambda: export_to_png(self.painter.canvas, root),
            "svg": lambda: export_to_svg(self.painter.canvas, root),
            "eps": lambda: export_to_eps(self.painter.canvas)
            })
        
        self.frame1 = tk.Frame(
            self, 
            width=50, 
            height=self.master.winfo_height())
        
        self.frame2 = tk.Frame(
            self, 
            height=30, 
            width=self.master.winfo_width())
        
        self.frame1.grid(column=0, row=1)
        self.frame2.grid(column=0, row=0)


root = tk.Tk()


# def drag(event):
#     app.painter.handle_drag(event)


def left_click(event):
    app.painter.handle_left_click(event)


def button_release(event):
    app.painter.handle_btn_release()


def right_click(event):
    app.painter.handle_right_click(event)


def handle_key_press(event):
    app.painter.handle_typing(event)


root.geometry('830x580')
root.resizable(False, False)


root.bind('<Button-1>', left_click)
root.bind('<ButtonRelease-1>', button_release)
root.bind('<Button-3>', right_click)
root.bind('<Key>', handle_key_press)

app = Application(master=root)
app.mainloop()
