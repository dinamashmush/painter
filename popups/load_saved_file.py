from typing import *

import tkinter as tk

class LoadSavedFile(tk.Toplevel):
    """a popup to get the name of the file to load
    """
    def __init__(self, master: tk.Misc, load_json:Callable[[str],bool]) -> None:
        super().__init__(master)
        self.geometry("370x130+300+150")
        self.grab_set()
        
        self.title("Load Saved File")
        self.grid_columnconfigure(0, weight=1)
        
        self.label = tk.Label(self, text="Please enter a valid json file path.\n Please note that the current canvas will be deleted.")
        self.label.grid(column=0, row=0, sticky=tk.NSEW, columnspan=3)
        
        self.entry = tk.Entry(self, width=1)
        self.entry.grid(column=0, columnspan=2, row=2, sticky=tk.NSEW, padx=70, pady=10)
        
        def command() -> None:
            success = load_json(self.entry.get())
            if success:
                self.destroy()
            else:
                self.error_msg = tk.Label(self, text="invalid path or json file. please try again with a different file", fg="red")
                self.error_msg.grid(row=3, column=0, sticky=tk.NSEW, columnspan=3)
        
        self.load_btn = tk.Button(self, text="Load", command=command)
        self.load_btn.grid(row=4, column=0, sticky=tk.NSEW, padx=120)
