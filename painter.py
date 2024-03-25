from typing import *
import tkinter as tk
from enums import *
from stroke import Stroke
import math


class Painter(tk.Frame):
    def __init__(self, root, color: tk.StringVar, state: tk.StringVar, width: tk.IntVar) -> None:
        super().__init__(root)

        self.color = color
        self.state = state

        self.strokes: List[Stroke] = []
        self.canvas = tk.Canvas(root, width=640, height=480, bg="#000000")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.line_style: LineStyle = LineStyle.SOLID
        self.width = width

        self.curr_stroke: Union[Literal[None], Stroke] = None
        self.active_select_start: Union[Tuple[int, int], Literal[None]] = None
        self.active_select_end: Union[Tuple[int, int], Literal[None]] = None
        self.active_selection_rect: Union[int, Literal[None]] = None
        self.selected_strokes: List[int] = []  # indexes of selected strokes
        self.selected_rect: Union[Literal[None], int] = None
        self.selected_rect_locs: Union[Tuple[int, int, int, int], None] = None

        self.drag_strokes = False
        self.prev_x = 0
        self.prev_y = 0

        self.selected_menu = tk.Menu(self, tearoff=0)
        # self.m.add_command(label="Paste")
        self.selected_menu.add_command(label="Copy")
        self.selected_menu.add_command(label="Change Properties")
        self.selected_menu.add_command(label="Move Forward", command=lambda: self.move_forward_backward_selected(True))
        self.selected_menu.add_command(label="Move Backward", command=lambda:self.move_forward_backward_selected(False))
        self.selected_menu.add_separator()
        self.selected_menu.add_command(label="Delete", command=self.delete_selected)
        
    def move_forward_backward_selected(self, forward:bool) -> None:
        selected_strokes = [self.strokes[i] for i in self.selected_strokes]
        not_selected_strokes = [stroke for i, stroke in enumerate(self.strokes) if i not in self.selected_strokes]
        
        self.strokes = not_selected_strokes + selected_strokes if forward else selected_strokes + not_selected_strokes
        self.selected_strokes = list(range(len(self.strokes) - len(selected_strokes), len(self.strokes))) if forward else list(range(len(selected_strokes)))
        for stroke in self.strokes:
            stroke.paint()
        
        

    def handle_drag(self, event):
        if self.drag_strokes:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y

            self.canvas.delete(self.selected_rect)
            self.selected_rect_locs = self.selected_rect_locs[0] + dx, self.selected_rect_locs[1] + \
                dy, self.selected_rect_locs[2] + \
                dx, self.selected_rect_locs[3] + dy
            self.selected_rect = self.canvas.create_rectangle(
                *self.selected_rect_locs, outline="green")
            for i, stroke in enumerate(self.strokes):
                if i < min(self.selected_strokes): 
                    continue
                if i in self.selected_strokes:
                    stroke.move(dx, dy)
                else:
                    stroke.paint()
            # for stroke in [self.strokes[i] for i in self.selected_strokes]:
            #     stroke.move(dx, dy)
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
                    event.x, event.y, self.line_style, self.color.get(), self.width.get(), self.canvas)
                self.strokes.append(new_stroke)
                self.curr_stroke = new_stroke
            else:
                self.curr_stroke.continue_stroke(event.x, event.y)
        elif self.state.get() == State.SELECT.value:

            if not self.active_select_start:
                self.remove_select()
                self.active_select_start = (event.x, event.y)
            else:
                if self.active_selection_rect:
                    self.canvas.delete(self.active_selection_rect)
                self.active_selection_rect = self.canvas.create_rectangle(
                    *self.active_select_start, event.x, event.y, outline="#fff")
                self.active_select_end = (event.x, event.y)

        # elif self.state.get() == State.ERASE.value:
        #     for stroke in self.strokes or stroke:
        #         if (event.x, event.y) in stroke.coordinates:
        #             stroke.delete()
        #             index = stroke.coordinates.index((event.x, event.y))
        #             if index != (len(stroke.coordinates) - 1):
        #                 new_stroke2 = Stroke(
        #                     *stroke.coordinates[index+1], stroke.line_style, 'red', stroke.width, self.canvas)
        #                 new_stroke2.coordinates = stroke.coordinates[index + 1:]
        #                 new_stroke2.paint()
        #                 self.strokes.append(new_stroke2)

        #             new_stroke1 = Stroke(
        #                 *stroke.coordinates[0], stroke.line_style, 'blue', stroke.width, self.canvas)
        #             new_stroke1.coordinates = stroke.coordinates[:index]
        #             new_stroke1.paint()
        #             self.strokes.append(new_stroke1)

        #             self.strokes.remove(stroke)

    def remove_select(self) -> None:
        self.selected_strokes = []
        if (self.selected_rect):
            self.canvas.delete(self.selected_rect)

    def handle_left_click(self, event) -> None:
        if not self.selected_rect_locs:
            return
        if not (event.x >= self.selected_rect_locs[0] and event.x <= self.selected_rect_locs[2] and event.y >= self.selected_rect_locs[1] and event.y <= self.selected_rect_locs[3]):
            self.remove_select()

    def handle_stop_drag(self) -> None:
        if self.drag_strokes:
            self.drag_strokes = False
        if self.state.get() == State.PAINT.value:
            self.curr_stroke = None
        elif self.state.get() == State.SELECT.value:
            if self.active_selection_rect:
                self.canvas.delete(self.active_selection_rect)
            self.select_by_rect()
            self.active_select_start = None
            self.active_select_end = None

    def select_by_rect(self) -> None:
        if not self.active_select_start or not self.active_select_end:
            return
        rect_range_x = range(min(self.active_select_start[0], self.active_select_end[0]),
                             max(self.active_select_start[0], self.active_select_end[0]))
        rect_range_y = range(min(self.active_select_start[1], self.active_select_end[1]),
                             max(self.active_select_start[1], self.active_select_end[1]))

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
        self.selected_rect_locs = (min_x, min_y, max_x, max_y)

    def handle_right_click(self, event: tk.Event) -> None:
        if len(self.selected_strokes) > 0 and self.selected_rect_locs:
            if event.x > self.selected_rect_locs[0] and event.x < self.selected_rect_locs[2] and event.y > self.selected_rect_locs[1] and event.y < self.selected_rect_locs[3]:
                try:
                    self.selected_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    self.selected_menu.grab_release()
    def delete_selected(self) -> None:
        for stroke in [self.strokes[i] for i in self.selected_strokes]:
            stroke.delete()
            self.strokes.remove(stroke)
        self.remove_select()