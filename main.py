import tkinter as tk
from toolbar import ToolBar
from math import *
from typing import *
from painter import Painter
from enums import State



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.color = tk.StringVar(self, "#ffffff")
        self.state = tk.StringVar(self, State.PAINT.value)
        self.width = tk.IntVar(self, 3)

        self.create_widgets()

    def create_widgets(self):
        self.painter = Painter(self, color=self.color, state=self.state, width=self.width)
        self.toolbar = ToolBar(self, color=self.color, state=self.state, width=self.width)
        

root = tk.Tk()



def drag(event):
    app.painter.handle_drag(event)

def left_click(event):
    app.painter.handle_left_click(event)

def button_release(event):
    app.painter.handle_stop_drag()

root.bind('<B1-Motion>', drag)
root.bind('<Button-1>', left_click)
root.bind('<ButtonRelease-1>', button_release)
app = Application(master=root)
app.mainloop()
