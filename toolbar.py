import tkinter as tk

from typing import *
from PIL import Image, ImageTk

from enums import State
from popups.text_options import TextOptions
from helper_funcs.validate_funcs import validate_width
from helper_funcs.load_available_fonts import load_available_fonts
from components.color_btn import ColorBtn
from components.tooltip import Tooltip
from components.icon_button import IconButton
from popups.load_saved_file import LoadSavedFile

class ToolBar(tk.Frame):
    """the toolbar - controlling drawing tools and options.
    """
    def __init__(self, root: tk.Misc, color: tk.StringVar, fill:tk.StringVar, state: tk.StringVar, width: tk.IntVar, bold: tk.BooleanVar, italic: tk.BooleanVar, export: Dict[str, Callable], font: tk.StringVar, font_size: tk.IntVar, delete_all: Callable, save_to_json:Callable, load_json:Callable, undo:Callable, redo:Callable) -> None:
        super().__init__(root)
        self.root = root
        self.grid(row=1, column=2, padx=(10, 30), pady=(40, 30))
        
        self.color = color
        self.fill = fill
        self.width = width
        self.font = font
        self.font_size = font_size
        self.italic = italic
        self.bold = bold

        self.state = state
        
        self.export = export
        self.delete_all = delete_all
        self.save_to_json = save_to_json
        self.load_json = load_json
        self.undo = undo
        self.redo = redo
        
        self.create_widgets()
        
    def change_selected_state(self, state: str, btn: tk.Button) -> None:
        """
        Change the selected drawing state.

        Args:
            state (str): The new drawing state.
            btn (tk.Button): The button associated with the new state.
        """

        if self.state.get() == State.PAINT.value and state == State.PAINT.value:
            return
        for button in [self.select_button, self.oval_btn, self.rect_btn, self.text_btn, self.polygon_btn, self.triangle_btn, self.freestyle_button]:
            button.config(relief="raised")
        if self.state.get() == state: 
            self.state.set(State.PAINT.value)
            btn.config(relief="raised")
            self.freestyle_button.config(relief="sunken")
        else:
            self.state.set(state)
            btn.config(relief="sunken")


    def create_widgets(self) -> None:
        """
        Create the toolbar widgets.
        """

        self.export_menu = tk.Menu(self, tearoff=0)
        self.export_menu.add_command(label="png", command=self.export["png"])
        self.export_menu.add_command(label="svg", command=self.export["svg"])
        self.export_menu.add_command(label="eps", command=self.export["eps"])

        def open_export_menu() -> None:
            try:
                self.export_menu.tk_popup(self.export_btn.winfo_rootx(), self.export_btn.winfo_rooty())
            finally:
                self.export_menu.grab_release()

        
        self.export_btn = tk.Button(self, text="Export As", command=open_export_menu)
        self.export_btn.pack()
        
        self.save_frame = tk.Frame(self)
        self.save_frame.pack(pady=5)
        
                
        info_icon_image = Image.open("./assets/information.png")
        resize_info_icon = info_icon_image.resize((16, 16))
        self.info_icon = ImageTk.PhotoImage(resize_info_icon)
        self.info_button = tk.Label(self.save_frame,  image=self.info_icon, compound="left")
        self.tooltip = Tooltip(self.info_button, "This will save the current drawing in a json file.\nThe json file will be called canvas-data-<curr-time>.json.\nYou can later load the saved canvas using\n the load saved file button.")

        self.save_btn = tk.Button(self.save_frame, text="Save", command=self.save_to_json)
        self.save_btn.pack(side=tk.LEFT)
        self.info_button.pack(side=tk.LEFT, padx=3)
        
        self.load_json_btn = tk.Button(self, text="Load Saved File", command=lambda:LoadSavedFile(self, self.load_json) )
        self.load_json_btn.pack()
        
        self.separator0 = tk.Frame(self, height=1,background="gray")
        self.separator0.pack(fill="x", pady=10)
        
        self.undo_frame = tk.Frame(self)
        self.undo_frame.pack()
        
        self.undo_button = IconButton(self.undo_frame, img_path="./assets/undo.png", img_size=16, command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=3)
        
        self.undo_button = IconButton(self.undo_frame, img_path="./assets/redo.png", img_size=16, command=self.redo)
        self.undo_button.pack(side=tk.LEFT, padx=3)
        
        self.separator1 = tk.Frame(self, height=1,background="gray")
        self.separator1.pack(fill="x", pady=10)
        
        self.color_btn = ColorBtn(self, text = "Color", color=self.color.get(), on_change=lambda color: self.color.set(color))
        self.color_btn.pack()
        
        self.fill_frame = tk.Frame(self)
        self.fill_frame.pack(pady=5)
        
        self.fill_btn = ColorBtn(self.fill_frame, text = "Fill", color=self.fill.get(), on_change=lambda color: self.fill.set(color))
        self.fill_btn.pack(side=tk.LEFT)
        
        def no_fill_command() -> None:
            self.fill.set("")
            self.fill_btn.configure(image="")
        
        self.no_fill_btn: tk.Button = tk.Button(self.fill_frame, text="no fill", command=no_fill_command)
        self.no_fill_btn.pack(side=tk.LEFT)
        
        self.width_frame = tk.Frame(self)
        self.width_frame.pack(pady=5)
        
        self.width_label = tk.Label(self.width_frame, text="Line Width: ")
        self.width_label.pack(side=tk.LEFT)
        
        validatecommand = (self.register(validate_width))
        self.width_input = tk.Spinbox(self.width_frame, textvariable=self.width, from_=1, to=9, increment=1, validatecommand=(validatecommand,'%P'), validate="all", width=2) 
        self.width_input.pack(side=tk.LEFT)
        
        self.separator2 = tk.Frame(self, height=1,background="gray")
        self.separator2.pack(fill="x", pady=5)

        self.select_button = IconButton(self, text="Select", img_path="./assets/3793488.png", img_size=16, command=lambda: self.change_selected_state(State.SELECT.value, self.select_button))
        self.select_button.pack(pady=5)
        
        self.freestyle_button = IconButton(self, img_path="./assets/pencil.png", img_size=22, command=lambda: self.change_selected_state(State.PAINT.value, self.freestyle_button) ,btn_size=24 )
        self.freestyle_button.pack(pady=5)
        self.freestyle_button.configure(relief="sunken")
        
        self.create_shapes_btns()
        
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(pady=5)
                
        self.text_btn = IconButton(self.text_frame, img_path="./assets/icons-text.png",img_size=24, command=lambda: self.change_selected_state(State.TEXT.value, self.text_btn))
        self.text_btn.pack(side=tk.LEFT, padx=5)
        
        def on_save(font:str, font_size:int, color:str, bold: bool, italic: bool) -> None:
            fonts = load_available_fonts()
            if font in fonts:
                self.font.set(font)
            else:
                self.font.set("Arial")

            self.font_size.set(font_size)
            self.color.set(color)
            self.bold.set(bold)
            self.italic.set(italic)
        
        self.text_options_btn = tk.Button(self.text_frame,
                                          command=lambda: TextOptions(self.root, 
                                                                      color=self.color.get(), 
                                                                      font_size=self.font_size.get(), 
                                                                      font=self.font.get(),
                                                                      bold=self.bold.get(),
                                                                      italic=self.italic.get(),
                                                                      on_save=on_save), 
                                          text="Text\nOptions")
        self.text_options_btn.pack(side=tk.LEFT)

        self.separator3 = tk.Frame(self, height=1,background="gray")
        self.separator3.pack(fill="x", pady=5)

        
        self.delete_all_btn = tk.Button(self, text="Clear\nCanvas", command=self.delete_all)
        self.delete_all_btn.pack()

    def create_shapes_btns(self) -> None:
        """
        Create buttons for selecting different shapes.
        """
        
        self.shapes_frame1 = tk.Frame(self)
        self.shapes_frame1.pack()
        self.shapes_frame2 = tk.Frame(self)
        self.shapes_frame2.pack()

        
        self.oval_btn = IconButton(self.shapes_frame1, img_path="./assets/icons-circle.png", img_size=24, command=lambda: self.change_selected_state(State.OVAL.value, self.oval_btn))
        self.oval_btn.pack(side=tk.LEFT, padx=3, pady=3)
        
        self.rect_btn = IconButton(self.shapes_frame1, img_path="./assets/icons-square.png",img_size=24, command=lambda: self.change_selected_state(State.RECT.value, self.rect_btn))
        self.rect_btn.pack(side=tk.LEFT, padx=3, pady=3)

        self.polygon_btn = IconButton(self.shapes_frame2, img_path="./assets/polygon.png", img_size=24, command=lambda: self.change_selected_state(State.POLYGON.value, self.polygon_btn))
        self.polygon_btn.pack(side=tk.LEFT, padx=3, pady=3)
        
        self.triangle_btn = IconButton(self.shapes_frame2, img_path="./assets/triangle.png", img_size=24, command=lambda: self.change_selected_state(State.TRIANGLE.value, self.triangle_btn))
        self.triangle_btn.pack(side=tk.LEFT, padx=3, pady=3)
         
