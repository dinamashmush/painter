from typing import *
import tkinter as tk
from enums import *


class Painter(tk.Frame):
    def __init__(self, root, color: tk.StringVar, state:tk.StringVar) -> None:
        super().__init__(root)

        self.curr_stroke: Union[Literal[None], Stroke] = None
        self.strokes: List[Stroke] = []
        self.canvas = tk.Canvas(root, width=640, height=480, bg="#000000")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.color = color
        self.line_style: LineStyle = LineStyle.SOLID
        self.width = 3
        self.state = state
        self.active_selection_start_coordinates:Union[Tuple[int, int], Literal[None]] = None
        self.active_selection_end_coordinates:Union[Tuple[int,int], Literal[None]] = None
        self.active_selection_rect:Union[int, Literal[None]] = None

    def handle_drag(self, event):
        
        if self.state.get() == State.PAINT.value:
            if not self.curr_stroke:
                new_stroke = Stroke(
                    event.x, event.y, self.line_style, self.color, self.width)
                self.strokes.append(new_stroke)
                self.curr_stroke = new_stroke
            else:
                self.canvas.create_line(*self.curr_stroke.coordinates[-1],
                                        event.x, event.y,
                                        fill=self.color.get(),
                                        width=self.width,
                                        smooth=True)
                self.curr_stroke.continue_stroke(event.x, event.y)
        elif self.state.get() == State.SELECT.value:
            if not self.active_selection_start_coordinates:
                print("here2")
                self.active_selection_start_coordinates = (event.x, event.y)
            else:
                print("here")
                if self.active_selection_rect: self.canvas.delete(self.active_selection_rect)
                self.active_selection_rect = self.canvas.create_rectangle(*self.active_selection_start_coordinates, event.x, event.y, outline="#fff")
                self.active_selection_end_coordinates = (event.x, event.y)

    def handle_stop_drag(self) -> None:
        if self.state.get() == State.PAINT.value:
            self.curr_stroke = None
        elif self.state.get() == State.SELECT.value:
            self.active_selection_start_coordinates = None


class Stroke():
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int) -> None:
        self.line_style = line_style
        self.color = color
        self.coordinates: List[Tuple[int, int]] = [(x, y)]
        self.width = width

    def continue_stroke(self, x: int, y: int) -> None:
        self.coordinates.append((x, y))
