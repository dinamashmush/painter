import tkinter as tk
from typing import *
from PIL import Image, ImageTk

from enums import State
from text_options import TextOptions
from validate_funcs import validate_width
from color_btn import ColorBtn
from tooltip import Tooltip
from load_saved_file import LoadSavedFile

class ToolBar(tk.Frame):
    def __init__(self, root, color: tk.StringVar, fill:tk.StringVar, state: tk.StringVar, width: tk.IntVar, export: Dict[str, Callable], font: tk.StringVar, font_size: tk.IntVar, delete_all: Callable, save_to_json:Callable, load_json:Callable):
        super().__init__(root)
        self.root = root
        self.grid(row=1, column=2, padx=(10, 0))
        self.color = color
        self.fill = fill
        self.state = state
        self.width = width
        self.export = export
        self.font = font
        self.font_size = font_size
        self.delete_all = delete_all
        self.save_to_json = save_to_json
        self.load_json = load_json
        self.create_widgets()
        
    def change_selected_state(self, state: str, btn: tk.Button) -> None:
        for button in [self.select_button, self.oval_btn, self.rect_btn, self.text_btn, self.polygon_btn, self.triangle_btn]:
            button.config(relief="raised")
        if self.state.get() == state: 
            self.state.set(State.PAINT.value)
            btn.config(relief="raised")
        else:
            self.state.set(state)
            btn.config(relief="sunken")


    def create_widgets(self) -> None:
        
        self.export_menu = tk.Menu(self, tearoff=0)
        self.export_menu.add_command(label="png", command=self.export["png"])
        self.export_menu.add_command(label="svg", command=self.export["svg"])
        self.export_menu.add_command(label="eps", command=self.export["eps"])

        def open_export_menu():
            try:
                self.export_menu.tk_popup(self.export_btn.winfo_rootx(), self.export_btn.winfo_rooty())
            finally:
                self.export_menu.grab_release()

        
        self.export_btn = tk.Button(self, text="Export As", command=open_export_menu)
        self.export_btn.pack(pady=10)
        
        self.save_frame = tk.Frame(self)
        self.save_frame.pack(pady=10)
        
                
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
        
        self.color_btn = ColorBtn(self, text = "Color", color=self.color.get(), on_change=lambda color: self.color.set(color))
        self.color_btn.pack(pady=10)
        
        self.fill_frame = tk.Frame(self)
        self.fill_frame.pack(pady=10)
        
        self.fill_btn = ColorBtn(self.fill_frame, text = "Fill", color=self.fill.get(), on_change=lambda color: self.fill.set(color))
        self.fill_btn.pack(side=tk.LEFT)
        
        def no_fill_command() -> None:
            self.fill.set("")
            self.fill_btn.configure(image="")
        
        self.no_fill_btn: tk.Button = tk.Button(self.fill_frame, text="no fill", command=no_fill_command)
        self.no_fill_btn.pack(side=tk.LEFT)
        
        select_icon_image = Image.open("./assets/3793488.png")
        resize_select_icon = select_icon_image.resize((16, 16))
        self.select_icon = ImageTk.PhotoImage(resize_select_icon)
        self.select_button = tk.Button(self, text="Select", image=self.select_icon, compound="left", command=lambda: self.change_selected_state(State.SELECT.value, self.select_button))
        self.select_button.pack(pady=10)
        
        self.width_frame = tk.Frame(self)
        self.width_frame.pack(pady=10)
        
        self.width_label = tk.Label(self.width_frame, text="Line Width: ")
        self.width_label.pack(side=tk.LEFT)
        
        validatecommand = (self.register(validate_width))
        self.width_input = tk.Spinbox(self.width_frame, textvariable=self.width, from_=1, to=9, increment=1, validatecommand=(validatecommand,'%P'), validate="all", width=2) 
        self.width_input.pack(side=tk.LEFT)
        
        self.create_shapes_btns()
        
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(pady=20)
                
        text_icon_image = Image.open("./assets/icons-text.png")
        resize_text_icon = text_icon_image.resize((24, 24))
        self.text_icon = ImageTk.PhotoImage(resize_text_icon)
        self.text_btn = tk.Button(self.text_frame, image=self.text_icon, command=lambda: self.change_selected_state(State.TEXT.value, self.text_btn))
        self.text_btn.pack(side=tk.LEFT, padx=5)
        
        def on_save(font:str, font_size:int, color:str):
            self.font.set(font)
            self.font_size.set(font_size)
            self.color.set(color)
        
        self.text_options_btn = tk.Button(self.text_frame,command=lambda: TextOptions(self.root, color=self.color.get(), font_size=self.font_size.get(), font=self.font.get(), on_save=on_save), text="Text\nOptions")
        self.text_options_btn.pack(side=tk.LEFT)

        
        self.delete_all_btn = tk.Button(self, text="Clear\nCanvas", command=self.delete_all)
        self.delete_all_btn.pack()

    def create_shapes_btns(self) -> None:
        
        self.shapes_frame1 = tk.Frame(self)
        self.shapes_frame1.pack()
        self.shapes_frame2 = tk.Frame(self)
        self.shapes_frame2.pack()

        
        oval_icon_image = Image.open("./assets/icons-circle.png")
        resize_oval_icon = oval_icon_image.resize((24, 24))
        self.resize_oval_icon = ImageTk.PhotoImage(resize_oval_icon)
        self.oval_btn = tk.Button(self.shapes_frame1, image=self.resize_oval_icon, command=lambda: self.change_selected_state(State.OVAL.value, self.oval_btn))
        self.oval_btn.pack(side=tk.LEFT, padx=3, pady=3)
        
        rect_icon_image = Image.open("./assets/icons-square.png")
        resize_rect_icon = rect_icon_image.resize((24, 24))
        self.resize_rect_icon = ImageTk.PhotoImage(resize_rect_icon)
        self.rect_btn = tk.Button(self.shapes_frame1, image=self.resize_rect_icon, command=lambda: self.change_selected_state(State.RECT.value, self.rect_btn))
        self.rect_btn.pack(side=tk.LEFT, padx=3, pady=3)

        polygon_icon_image = Image.open("./assets/polygon.png")
        resize_polygon_icon = polygon_icon_image.resize((24, 24))
        self.resize_polygon_icon = ImageTk.PhotoImage(resize_polygon_icon)
        self.polygon_btn = tk.Button(self.shapes_frame2, image=self.resize_polygon_icon, command=lambda: self.change_selected_state(State.POLYGON.value, self.polygon_btn))
        self.polygon_btn.pack(side=tk.LEFT, padx=3, pady=3)
        
        triangle_icon_image = Image.open("./assets/triangle.png")
        resize_triangle_icon = triangle_icon_image.resize((24, 24))
        self.resize_triangle_icon = ImageTk.PhotoImage(resize_triangle_icon)
        self.triangle_btn = tk.Button(self.shapes_frame2, image=self.resize_triangle_icon, command=lambda: self.change_selected_state(State.TRIANGLE.value, self.triangle_btn))
        self.triangle_btn.pack(side=tk.LEFT, padx=3, pady=3)
         
