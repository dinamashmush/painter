import tkinter as tk
from toolbar import ToolBar
from math import *
from typing import *
from painter import Painter
from enums import State
WIDTH, HEIGHT = 640, 480



def left_click(event):
    print("Left button clicked")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.color = tk.StringVar(self, "#000000")
        self.state = tk.StringVar(self, State.SELECT.value)

        self.create_widgets()

    def create_widgets(self):
        self.painter = Painter(self, self.color, self.state)
        self.toolbar = ToolBar(self, self.color, self.state)
        

root = tk.Tk()



def drag(event):
    app.painter.handle_drag(event)

def button_release(event):
    app.painter.handle_stop_drag()

root.bind('<B1-Motion>', drag)
root.bind('<Button-1>', left_click)
root.bind('<ButtonRelease-1>', button_release)
app = Application(master=root)
app.mainloop()
