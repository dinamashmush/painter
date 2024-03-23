from typing import *
import tkinter as tk
from enums import *


class Painter(tk.Frame):
    def __init__(self, root, color: tk.StringVar, state: tk.StringVar) -> None:
        super().__init__(root)

        self.color = color
        self.state = state

        self.strokes: List[Stroke] = []
        self.canvas = tk.Canvas(root, width=640, height=480, bg="#000000")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.line_style: LineStyle = LineStyle.SOLID
        self.width = 3

        self.curr_stroke: Union[Literal[None], Stroke] = None
        self.active_selection_start: Union[Tuple[int,
                                                 int], Literal[None]] = None
        self.active_selection_end: Union[Tuple[int, int], Literal[None]] = None
        self.active_selection_rect: Union[int, Literal[None]] = None
        self.selected_strokes: List[int] = []  # indexes of selected strokes
        self.selected_rect: Union[Literal[None], int] = None
        self.selected_rect_locs: Union[Tuple[int, int, int, int], None] = None

        self.drag_strokes = False
        self.prev_x = 0
        self.prev_y = 0

    def handle_drag(self, event):
        if self.drag_strokes:
            dx =  event.x - self.prev_x
            dy =  event.y - self.prev_y

            self.canvas.delete(self.selected_rect)
            self.selected_rect_locs = self.selected_rect_locs[0] + dx, self.selected_rect_locs[1] + dy, self.selected_rect_locs[2] + dx, self.selected_rect_locs[3] + dy
            self.selected_rect = self.canvas.create_rectangle(*self.selected_rect_locs, outline="green")
            for stroke in [self.strokes[i] for i in self.selected_strokes]:
                stroke.move(dx, dy)
            self.prev_x = event.x
            self.prev_y = event.y

                
            return

        if len(self.selected_strokes):
            if event.x >= self.selected_rect_locs[0] and event.x <= self.selected_rect_locs[2] and event.y >= self.selected_rect_locs[1] and event.y <= self.selected_rect_locs[3]:
                self.drag_strokes = True
                self.prev_x = event.x
                self.prev_y = event.y
                return
        if self.state.get() == State.PAINT.value:
            if not self.curr_stroke:
                new_stroke = Stroke(
                    event.x, event.y, self.line_style, self.color.get(), self.width, self.canvas)
                self.strokes.append(new_stroke)
                self.curr_stroke = new_stroke
            else:
                self.curr_stroke.continue_stroke(event.x, event.y)
        elif self.state.get() == State.SELECT.value:

            if not self.active_selection_start:
                self.remove_select()
                self.active_selection_start = (event.x, event.y)
            else:
                if self.active_selection_rect:
                    self.canvas.delete(self.active_selection_rect)
                self.active_selection_rect = self.canvas.create_rectangle(
                    *self.active_selection_start, event.x, event.y, outline="#fff")
                self.active_selection_end = (event.x, event.y)

    def remove_select(self) -> None:
        self.selected_strokes = []
        if (self.selected_rect):
            self.canvas.delete(self.selected_rect)

    def handle_stop_drag(self) -> None:
        if self.drag_strokes:
            self.drag_strokes = False
        if self.state.get() == State.PAINT.value:
            self.curr_stroke = None
        elif self.state.get() == State.SELECT.value:
            if self.active_selection_rect:
                self.canvas.delete(self.active_selection_rect)
            self.select_by_rect()
            self.active_selection_start = None
            self.active_selection_end = None

    def select_by_rect(self) -> None:
        if not self.active_selection_start or not self.active_selection_end:
            return
        rect_range_x = range(min(self.active_selection_start[0], self.active_selection_end[0]),
                             max(self.active_selection_start[0], self.active_selection_end[0]))
        rect_range_y = range(min(self.active_selection_start[1], self.active_selection_end[1]),
                             max(self.active_selection_start[1], self.active_selection_end[1]))

        selected_rect = [(i, j) for i in rect_range_x for j in rect_range_y]

        for index, stroke in enumerate(self.strokes):
            if not set(selected_rect).isdisjoint(stroke.coordinates):
                stroke.set_selected(True)
                self.selected_strokes.append(index)
        if not len(self.selected_strokes):
            return
        selected_strokes = [self.strokes[i] for i in self.selected_strokes]
        stroke_coordinates = [
            i for stroke in selected_strokes for i in stroke.coordinates]
        stroke_x_coordinates = [stroke[0] for stroke in stroke_coordinates]
        stroke_y_coordinates = [stroke[1] for stroke in stroke_coordinates]
        min_x, max_x = min(stroke_x_coordinates), max(stroke_x_coordinates)
        min_y, max_y = min(stroke_y_coordinates), max(stroke_y_coordinates)
        self.selected_rect = self.canvas.create_rectangle(
            min_x, min_y, max_x, max_y, outline="green")
        self.selected_rect_locs = (min_x, min_y,max_x, max_y)


class Stroke():
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int, canvas: tk.Canvas) -> None:
        self.line_style = line_style
        self.color = color
        self.coordinates: List[Tuple[int, int]] = [(x, y)]
        self.width = width
        self.selected = False
        self.canvas = canvas
        self.lines: List[int] = []

    def continue_stroke(self, x: int, y: int) -> None:
        
        line = self.canvas.create_line(*self.coordinates[-1],
                                        x, y,
                                        fill=self.color,
                                        width=self.width,
                                        smooth=True)
        self.lines.append(line)
        self.coordinates.append((x, y))

    def set_selected(self, select: bool) -> None:
        self.selected = select
    def move(self, dx:int, dy:int) -> None:
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []
        new_coordinates: List[Tuple[int, int]] = []
        for i, co in enumerate(self.coordinates):
            x = co[0] + dx
            y = co[1] + dy
            if i != 0:
                line = self.canvas.create_line(*new_coordinates[i-1], x, y, fill=self.color)
                self.lines.append(line)
            new_coordinates.append((x, y))
        
        self.coordinates = new_coordinates
        
    
        
    
