import tkinter as tk
import json
from typing import *
from validate_funcs import validate_font_size

class TextOptions(tk.Toplevel):
    def __init__(self, master, font: str, font_size: int, on_save: Callable):
        super().__init__(master)
        self.geometry("500x250+150+150")
        
        self.font = font
        self.font_size = font_size
        self.on_save = on_save
        self.load_fonts_from_json()
        self.create_widgets()
        
    def load_fonts_from_json(self):
        json_fonts = open("assets/fonts.json")
        fonts = json.load(json_fonts)["fonts"]
        self.fonts = fonts
        
    def create_widgets(self) -> None:
        self.font_frame = tk.Frame(self)
        self.font_label1 = tk.Label(self.font_frame, text="font: ")
        self.font_entry = tk.Entry(self.font_frame)
        self.font_entry.insert(0, self.font) 
        
        self.font_frame.grid(column=0, row=0, sticky=tk.NW)
        self.font_label1.pack(side=tk.LEFT)
        self.font_entry.pack(side=tk.LEFT)
        
        self.font_listbox = tk.Listbox(self)
        self.font_listbox.insert(tk.END, *self.fonts)
        
        self.font_listbox_placeholder = tk.Frame(self, width=125, height=163)
        self.font_listbox_placeholder.grid(column=1, row=0)
        
        self.font_size_label = tk.Label(self, text="font size: ")
        
        validatecommand = (self.register(validate_font_size))

        self.font_size_spinbox = tk.Spinbox(self, from_=3, to=25, validatecommand=(validatecommand,'%P'), validate="all")
        self.font_size_spinbox.delete(0, "end")  
        self.font_size_spinbox.insert(0, str(self.font_size))
        
        self.font_size_label.grid(column=3, row=0, sticky=tk.NW)
        self.font_size_spinbox.grid(column=4, row=0, sticky=tk.NW)
        
        self.btns_frame = tk.Frame(self)
        self.btns_frame.grid(column=4, row=2, padx=(5, 0), pady=(50, 0))
        
        self.save_btn = tk.Button(self.btns_frame, command=self.save_changes, text="save")
        self.cancel_btn = tk.Button(self.btns_frame, command=self.destroy, text="cancel")
        self.save_btn.pack(side=tk.LEFT)
        self.cancel_btn.pack(padx=5, side=tk.LEFT)
        
        def get_font_listbox():
            self.font_listbox_placeholder.grid_forget()
            self.font_listbox.insert(tk.END, *self.fonts)
            self.font_listbox.grid(column=1, row=0)

        self.font_entry.bind("<FocusIn>", lambda _: get_font_listbox())
        self.font_entry.bind("<KeyRelease>", self.on_typing_font)
        self.font_listbox.bind("<Double-Button-1>", self.on_select_font)
        
    def save_changes(self) -> None:
        self.on_save(font=self.font_entry.get(), font_size=self.font_size_spinbox.get() if len(self.font_size_spinbox.get()) else self.font_size)
        self.destroy()

    def  on_typing_font(self, event) -> None:
        value = event.widget.get()
        if value:
            self.font_listbox.delete(0, tk.END)
            for item in self.fonts:
                if value.lower() in item.lower():
                    self.font_listbox.insert(tk.END, item)
        else:
            self.font_listbox.delete(0, tk.END)
            self.font_listbox.insert(tk.END, *self.fonts)

    
    def on_select_font(self, event):
        selected_item = event.widget.get(tk.ACTIVE)
        if not selected_item:
            return
        self.font_entry.delete(0, tk.END)
        self.font_entry.insert(tk.END, selected_item)
        self.font_listbox.delete(0, tk.END)
        self.font_listbox.grid_forget()
        self.font_listbox_placeholder.grid(column=1, row=0)



