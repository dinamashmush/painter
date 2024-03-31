import tkinter as tk

from math import *
from typing import *
import sys

from enums import State

from toolbar import ToolBar
from painter import Painter

from helper_funcs.export_funcs import *

class Application(tk.Frame):
    """main application
    """

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
        """create a painter and a toolbar
        """
        
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
            "png": self.painter.export_to_png,
            "svg": lambda: export_to_svg(self.painter.canvas, root),
            "eps": lambda: export_to_eps(self.painter.canvas)
            },
            delete_all=self.painter.delete_all,
            save_to_json=self.painter.save_to_json,
            load_json=self.painter.restore_data_from_json,
            undo=self.painter.undo,
            redo=self.painter.redo)


if len(sys.argv) >= 2 and sys.argv[1] == "--help":
    print("To run this program, simply run main.py using python3:")
    print("python3 main.py")
    print("no arguments needed.")
    
    
else:

    root = tk.Tk()

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
