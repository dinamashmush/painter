import tkinter as tk

from typing import *

from helper_funcs.validate_funcs import validate_font_size
from helper_funcs.load_available_fonts import load_available_fonts
from components.color_btn import ColorBtn
from components.icon_button import IconButton

class TextOptions(tk.Toplevel):
    """a popup to change text properties
    """
    def __init__(self, master, font: str, font_size: int, color:str, bold: bool, italic: bool, on_save: Callable, multiple:bool = False):
        super().__init__(master)
        self.geometry("550x300+150+150")
        self.grab_set()

        self.font = font
        self.font_size = font_size
        self.color = color
        self.bold = bold
        self.italic = italic
        
        self.on_save = on_save
        self.multiple = multiple

        self.fonts = load_available_fonts()
        self.create_widgets()
        
        
    def create_widgets(self) -> None:
        """create the widget for the popup
        """

        if self.multiple:
            self.warning_label = tk.Label(self, text="Please note that these changes will affect all selected shapes and freestyle strokes.")
            self.warning_label.grid(row=0, column=0, columnspan=4, pady=10)            
        
        self.font_frame = tk.Frame(self)
        self.font_label1 = tk.Label(self.font_frame, text="font: ")
        self.font_entry = tk.Entry(self.font_frame)
        self.font_entry.insert(0, self.font) 
        
        self.font_frame.grid(column=0, row=1, sticky=tk.NW)
        self.font_label1.pack(side=tk.LEFT)
        self.font_entry.pack(side=tk.LEFT)
        
        self.font_label = tk.Label(self, text="Please pick one of the available fonts,\n if you will input a font that is not available,\n arial will be picked as default.")
        self.font_label.grid(column=0, row=2)
        self.font_listbox = tk.Listbox(self)
        self.font_listbox.insert(tk.END, *self.fonts)
        
        self.font_listbox_placeholder = tk.Frame(self, width=125, height=163)
        self.font_listbox_placeholder.grid(column=1, row=1, rowspan=3)
        
        self.font_size_label = tk.Label(self, text="font size: ")
        
        validatecommand = (self.register(validate_font_size))

        self.font_size_spinbox = tk.Spinbox(self, from_=3, to=25, validatecommand=(validatecommand,'%P'), validate="all")
        self.font_size_spinbox.delete(0, "end")  
        self.font_size_spinbox.insert(0, str(self.font_size))
        
        self.font_size_label.grid(column=3, row=1, sticky=tk.NW)
        self.font_size_spinbox.grid(column=4, row=1, sticky=tk.NW)
        
        def set_color(color:str) -> None:
            self.color = color
        self.color_btn = ColorBtn(self, text="Color", color=self.color, on_change=set_color)
        self.color_btn.grid(column=3, row=2, pady=(15, 0))
        
        self.btns_options_frame = tk.Frame(self)
        self.btns_options_frame.grid(column=3, row=3)
        def set_italic() -> None:
            self.italic = not self.italic
            if self.italic:
                self.italic_btn.config(relief="sunken")
            else:
                self.italic_btn.config(relief="raised")
        def set_bold() -> None:
            self.bold = not self.bold
            if self.bold:
                self.bold_btn.config(relief="sunken")
            else:
                self.bold_btn.config(relief="raised")
        self.italic_btn = IconButton(self.btns_options_frame, img_path="./assets/italic.png", img_size=16, command=set_italic)
        self.bold_btn = IconButton(self.btns_options_frame, img_path="./assets/bold.png", img_size=16, command=set_bold)
        if self.italic:
            self.italic_btn.configure(relief="sunken")
        if self.bold:
            self.bold_btn.configure(relief="sunken")
        self.italic_btn.pack(padx=3, side=tk.LEFT)
        self.bold_btn.pack(padx=3, side=tk.LEFT)
        
        self.btns_frame = tk.Frame(self)
        self.btns_frame.grid(column=0, row=3, padx=(5, 0), pady=(130, 0))
        
        self.save_btn = tk.Button(self.btns_frame, command=self.save_changes, text="save")
        self.cancel_btn = tk.Button(self.btns_frame, command=self.destroy, text="cancel")
        self.save_btn.pack(side=tk.LEFT)
        self.cancel_btn.pack(padx=5, side=tk.LEFT)
        
        def get_font_listbox():
            self.font_listbox_placeholder.grid_forget()
            self.font_listbox.delete(0, tk.END)
            self.font_listbox.insert(tk.END, *self.fonts)
            self.font_listbox.grid(column=1, row=1, rowspan=3, padx=(0, 3))

        self.font_entry.bind("<FocusIn>", lambda _: get_font_listbox())
        self.font_entry.bind("<KeyRelease>", self.on_typing_font)
        self.font_listbox.bind("<Double-Button-1>", self.on_select_font)
        
    def save_changes(self) -> None:
        """save the changes and close the popup
        """
        self.on_save(font=self.font_entry.get(), 
                     font_size=int(self.font_size_spinbox.get()) if len(self.font_size_spinbox.get()) else self.font_size, 
                     color=self.color,
                     bold=self.bold,
                     italic=self.italic)
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
        self.font_listbox_placeholder.grid(column=1, row=1, rowspan=3)



