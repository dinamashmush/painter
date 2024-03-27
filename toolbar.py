import tkinter as tk
from tkinter import colorchooser
from typing import *
from PIL import Image, ImageTk, ImageGrab
from enums import State
from text_options import TextOptions

class ToolBar(tk.Frame):
    def __init__(self, root, color: tk.StringVar, fill:tk.StringVar, state: tk.StringVar, width: tk.IntVar, export: Dict[str, Callable], font: tk.StringVar, font_size: tk.IntVar):
        super().__init__(root)
        self.root = root
        self.grid(row=1, column=2)
        self.color = color
        self.fill = fill
        self.state = state
        self.width = width
        self.export = export
        self.font = font
        self.font_size = font_size
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
                # pass
            finally:
                self.export_menu.grab_release()

        
        self.export_btn = tk.Button(self, text="Export As", command=open_export_menu)
        self.export_btn.pack(pady=10)

        data = bytes.fromhex(" ".join([self.color.get()[1:]]*(16*16)))
        img = Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
        self.color_img = ImageTk.PhotoImage(img)
        self.color_btn: tk.Button = tk.Button(self, text = "Color", image=self.color_img, compound="left",
                   command = self.update_color)
        self.color_btn.pack(pady=10)
        
        self.fill_frame = tk.Frame(self)
        self.fill_frame.pack(pady=10)
                
        self.fill_btn: tk.Button = tk.Button(self.fill_frame, text = "Fill", compound="left",
                   command = self.update_fill)
        self.fill_btn.pack(side=tk.LEFT)
        
        self.no_fill_btn: tk.Button = tk.Button(self.fill_frame, text="no fill", command=lambda: self.update_fill(True))
        self.no_fill_btn.pack(side=tk.LEFT)
    
        
        
        select_icon_image = Image.open("./assets/3793488.png")
        resize_select_icon = select_icon_image.resize((16, 16))
        self.select_icon = ImageTk.PhotoImage(resize_select_icon)
        self.select_button = tk.Button(self, text="Select", image=self.select_icon, compound="left", command=lambda: self.change_selected_state(State.SELECT.value, self.select_button))
        self.select_button.pack(pady=10)
        
        validatecommand = (self.register(self.validate_num))
        self.width_input = tk.Spinbox(self, textvariable=self.width, from_=1, to=9, increment=1, validatecommand=(validatecommand,'%P'), validate="all") 
        self.width_input.pack(pady=10)
        
        self.create_shapes_btns()
        
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(pady=20)
                
        text_icon_image = Image.open("./assets/icons-text.png")
        resize_text_icon = text_icon_image.resize((24, 24))
        self.text_icon = ImageTk.PhotoImage(resize_text_icon)
        self.text_btn = tk.Button(self.text_frame, image=self.text_icon, command=lambda: self.change_selected_state(State.TEXT.value, self.text_btn))
        self.text_btn.pack(side=tk.LEFT, padx=5)
        
        self.text_options_btn = tk.Button(self.text_frame,command=lambda: TextOptions(self.root, font_size=self.font_size, font=self.font), text="Text\nOptions")
        self.text_options_btn.pack(side=tk.LEFT)


    def validate_num(self, P):
        if len(P)>1:
            return False
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

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
         

    def pick_color(self) -> Union[Literal[None], Tuple[str, Image.Image]]:
        color = colorchooser.askcolor(title ="Choose color")[1]
        if not color: return None #!error message
        data = bytes.fromhex(" ".join([color[1:]]*(16*16)))
        return color, Image.frombuffer("RGB", (16, 16), data, "raw", "RGB", 0, 1)
        

    def update_color(self) -> None:
        picked_color = self.pick_color()
        if not picked_color:
            return
        color, img = picked_color
        self.color.set(color)
        self.color_img = ImageTk.PhotoImage(img)
        self.color_btn.config(image=self.color_img)

    def update_fill(self, delete: bool=False) -> None:
        if delete:
            color = ""
            self.fill_btn.config(image="")
        else:
            picked_color = self.pick_color()
            if not picked_color:
                return
            color, img = picked_color
            self.fill_img = ImageTk.PhotoImage(img)
            self.fill_btn.config(image=self.fill_img)
        self.fill.set(color)

    
    def say_hi(self):
        print("hi there, everyone!")
