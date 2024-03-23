import tkinter as tk
from typing import *

class DropDown():
    def __init__(self, root, options:List[str], value:tk.StringVar, options_images: List[tk.PhotoImage] = []):
        self.options = options
        self.options_images = options_images
        self.value = value
        self.root = root
        self.button = tk.Button(root, text="Select an option", width=10, relief="groove")
        self.button.bind("<Button-1>", self.show_menu)
        self.button.pack()

    def show_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        for i, option in enumerate(self.options):
            def on_changee(value=option):
                self.value.set(value)
                self.button.config(text=value, image=self.options_images[self.options.index(value)] if self.options_images else "", compound="left")
                self.button.config(width=100, relief="groove")

            menu.add_command(label=option, image=self.options_images[i] if self.options_images else "", compound="left",
                            command=on_changee)
        menu.post(event.x_root, event.y_root)

