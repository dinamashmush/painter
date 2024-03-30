from copy import copy
from typing import *
import json
from datetime import datetime
import os.path

import tkinter as tk
from PIL import Image, ImageDraw, ImageFont

from stroke import *
from action import *
from enums import *
from helper_funcs.calc_points_funcs import *
from helper_funcs.load_available_fonts import load_available_fonts
from popups.shape_options import ShapeOptions
from popups.text_options import TextOptions


class Painter(tk.Frame):
    def __init__(self, master, root, color: tk.StringVar, fill: tk.StringVar, state: tk.StringVar, width: tk.IntVar, font: tk.StringVar, font_size: tk.IntVar) -> None:
        super().__init__(master)

        self.grid(row=1, column=1)

        self.root = root

        self.color = color
        self.fill = fill
        self.state = state
        self.font = font
        self.font_size = font_size

        self.strokes: List[Stroke] = []
        self.groups: Set[FrozenSet[Stroke]] = set()
        self.canvas = tk.Canvas(self, width=640, height=480, bg="#000000")
        self.canvas.pack()

        self.line_style: LineStyle = LineStyle.SOLID
        self.width = width

        self.curr_stroke: Union[Literal[None], Stroke] = None

        self.actions: List[Action] = []
        self.undo_actions: List[Action] = []

        self.active_select_start: Union[Tuple[int, int], Literal[None]] = None
        self.active_select_end: Union[Tuple[int, int], Literal[None]] = None
        self.active_selection_rect: Union[int, Literal[None]] = None
        self.selected_strokes: List[Stroke] = []
        self.selected_rect: Union[Literal[None], int] = None
        self.selected_rect_locs: Union[Tuple[int, int, int, int], None] = None

        self.drag_strokes = False
        self.prev_x = 0
        self.prev_y = 0

        self.selected_menu = tk.Menu(self, tearoff=0)
        self.selected_menu.add_command(
            label="Copy", command=self.copy_selected)
        self.selected_menu.add_command(
            label="Move Forward", command=lambda: self.move_forward_backward_selected(True))
        self.selected_menu.add_command(
            label="Move Backward", command=lambda: self.move_forward_backward_selected(False))
        self.selected_menu.add_command(
            label="Delete", command=self.delete_selected)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Paste", command=self.pasted_copied)

        self.copied_strokes: Union[Literal[None], List[Stroke]] = None
        self.copied_bbox: Union[Literal[None],
                                Tuple[int, int, int, int]] = None
        self.paste_coordinates: Union[Literal[None], Tuple[int, int]] = None

        self.text_index: Union[Literal[None], int] = None
        self.curr_text_rect: Union[Literal[None], int] = None

        self.active_polygon_line: Union[Literal[None], int] = None

        self.canvas.bind('<Button-1>', self.handle_left_click_canvas)
        self.canvas.bind('<Motion>', self.handle_move_canvas)
        self.canvas.bind('<B1-Motion>', self.handle_drag)

    def undo(self) -> None:
        if not len(self.actions):
            return
        new_action = self.actions[-1].undo()
        self.actions.pop()
        self.undo_actions.append(new_action)

    def redo(self) -> None:

        if not len(self.undo_actions):
            return
        new_action = self.undo_actions[-1].redo()
        self.undo_actions.pop()
        self.actions.append(new_action)

    def move_forward_backward_selected(self, forward: bool) -> None:
        not_selected_strokes = [
            stroke for stroke in self.strokes if stroke not in self.selected_strokes]
        not_selected_strokes_indexes = [self.strokes.index(
            stroke) for stroke in self.strokes if stroke not in self.selected_strokes]
        if forward:
            self.strokes = not_selected_strokes + self.selected_strokes
            new_indexes = not_selected_strokes_indexes + \
                [i for i, _ in enumerate(
                    self.strokes) if i not in not_selected_strokes_indexes]
        else:
            self.strokes = self.selected_strokes + not_selected_strokes
            new_indexes = [i for i, _ in enumerate(
                self.strokes) if i not in not_selected_strokes_indexes] + not_selected_strokes_indexes
        self.actions.append(ChangeOrderAction(
            painter_strokes=self.strokes, og_indexes=new_indexes, canvas=self.canvas))
        for stroke in self.strokes:
            for i in stroke.tk_painting:
                self.canvas.tag_raise(i)

    def copy_selected(self) -> None:
        self.copied_strokes = []
        self.copied_bbox = self.canvas.bbox(
            *[p for stroke in self.selected_strokes for p in stroke.tk_painting])
        for stroke in self.selected_strokes:
            copied_stroke = copy(stroke)
            self.copied_strokes.append(copied_stroke)

    def pasted_copied(self) -> None:
        if not self.copied_strokes or not self.copied_bbox or not self.paste_coordinates:
            return
        copied_coordinates = (self.copied_bbox[0] + (((self.copied_bbox[2]) - self.copied_bbox[0])//2),
                              self.copied_bbox[1] + ((self.copied_bbox[3]-self.copied_bbox[1])//2))
        dx, dy = self.paste_coordinates[0] - \
            copied_coordinates[0], self.paste_coordinates[1] - \
            copied_coordinates[1]
        for stroke in self.copied_strokes:
            new_stroke = copy(stroke)
            new_stroke.coordinates = [(co[0] + dx, co[1] + dy)
                                      for co in new_stroke.coordinates]
            new_stroke.paint()
            self.strokes.append(new_stroke)

        self.undo_actions = []
        self.actions.append(CreateAction(
            painter_strokes=self.strokes, strokes=self.strokes[-len(self.copied_strokes):]))

    def handle_drag(self, event) -> None:

        if self.drag_strokes and self.selected_rect and self.selected_rect_locs:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y

            self.canvas.delete(self.selected_rect)
            self.selected_rect_locs = self.selected_rect_locs[0] + dx, self.selected_rect_locs[1] + \
                dy, self.selected_rect_locs[2] + \
                dx, self.selected_rect_locs[3] + dy
            self.selected_rect = self.canvas.create_rectangle(
                *self.selected_rect_locs, outline="green")
            started_paint_flag = False
            for stroke in self.strokes:
                if not started_paint_flag:
                    if stroke in self.selected_strokes:
                        started_paint_flag = True
                    else:
                        continue
                if stroke in self.selected_strokes:
                    stroke.move(dx, dy)
                else:
                    for i in stroke.tk_painting:
                        self.canvas.tag_raise(i)
            self.prev_x = event.x
            self.prev_y = event.y

            return

        if len(self.selected_strokes) and self.selected_rect_locs:
            if event.x >= self.selected_rect_locs[0] and event.x <= self.selected_rect_locs[2] and event.y >= self.selected_rect_locs[1] and event.y <= self.selected_rect_locs[3]:
                self.drag_strokes = True
                self.prev_x = event.x
                self.prev_y = event.y
                og_coordinates: List[Dict[str, Any]] = [{"coordinates": copy(
                    stroke.coordinates)} for stroke in self.selected_strokes]
                self.undo_actions = []
                self.actions.append(ChangePropAction(
                    painter_strokes=self.strokes, og_props=og_coordinates, strokes=[i for i in self.selected_strokes]))

                return

        if self.state.get() == State.PAINT.value:
            if not self.curr_stroke:
                new_stroke: Stroke = FreeStyleStroke(
                    event.x, event.y, self.line_style, self.color.get(), self.width.get(), self.canvas)
                self.strokes.append(new_stroke)
                self.curr_stroke = new_stroke
            else:
                self.curr_stroke.continue_stroke(event.x, event.y)
        elif self.state.get() == State.RECT.value:
            if not self.curr_stroke:
                new_stroke = ShapeStroke(event.x, event.y, self.line_style, self.color.get(
                ), self.width.get(), self.canvas, self.fill.get(), Shape.RECT)
                self.strokes.append(new_stroke)
                self.curr_stroke = new_stroke
            else:
                self.curr_stroke.continue_stroke(event.x, event.y)
        elif self.state.get() == State.OVAL.value:
            if not self.curr_stroke:
                new_stroke = ShapeStroke(event.x, event.y, self.line_style, self.color.get(
                ), self.width.get(), self.canvas, self.fill.get(), Shape.OVAL)
                self.strokes.append(new_stroke)
                self.curr_stroke = new_stroke
            else:
                self.curr_stroke.continue_stroke(event.x, event.y)
        elif self.state.get() == State.TRIANGLE.value:
            if not self.curr_stroke:
                new_stroke = TriangleStroke(event.x, event.y, self.line_style, self.color.get(
                ), self.width.get(), self.canvas, self.fill.get(), Shape.TRIANGLE)
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

    def remove_select(self) -> None:
        self.selected_strokes = []
        if (self.selected_rect):
            self.canvas.delete(self.selected_rect)

    def handle_left_click(self, event) -> None:
        self.remove_empty_text()
        if not self.selected_rect_locs:
            return
        if not (event.x >= self.selected_rect_locs[0] and event.x <= self.selected_rect_locs[2] and event.y >= self.selected_rect_locs[1] and event.y <= self.selected_rect_locs[3]):
            self.remove_select()

    def remove_empty_text(self) -> None:
        if isinstance(self.curr_stroke, TextStroke):
            if self.curr_text_rect:
                self.canvas.delete(self.curr_text_rect)
            if self.curr_stroke.text == "":
                self.curr_stroke.delete()
                self.strokes.pop()
            else:
                self.undo_actions = []
                self.actions.append(CreateAction(
                    painter_strokes=self.strokes, strokes=[self.curr_stroke]))

            self.curr_stroke = None

    def handle_left_click_canvas(self, event) -> Union[Literal[None], str]:
        self.root.focus()
        self.remove_empty_text()
        if self.state.get() == State.TEXT.value:
            self.create_text_stroke(event)
            return 'break'
        elif self.state.get() == State.POLYGON.value:
            if not self.curr_stroke:
                polygon = UnfinishedPolygonStroke(event.x, event.y, line_style=self.line_style, color=self.color.get(
                ), width=self.width.get(), canvas=self.canvas, fill=self.fill.get())
                self.curr_stroke = polygon
            else:
                self.curr_stroke.continue_stroke(event.x, event.y)
                for co in self.curr_stroke.coordinates[:-1]:
                    if abs(event.x - co[0]) < 5 and abs(event.y - co[1]) < 5:
                        if isinstance(self.curr_stroke, UnfinishedPolygonStroke):
                            polygon_stroke = self.curr_stroke.finish()
                            self.strokes.append(polygon_stroke)
                            self.curr_stroke = None
                            if self.active_polygon_line:
                                self.canvas.delete(self.active_polygon_line)
                            self.undo_actions = []
                            self.actions.append(CreateAction(
                                painter_strokes=self.strokes, strokes=[polygon_stroke]))
        return None

    def handle_move_canvas(self, event) -> None:
        if self.state.get() == State.POLYGON.value and self.curr_stroke:
            if self.active_polygon_line:
                self.canvas.delete(self.active_polygon_line)
            self.active_polygon_line = self.canvas.create_line(
                *self.curr_stroke.coordinates[-1], event.x, event.y, fill=self.color.get(), width=self.width.get())

    def create_text_stroke(self, event):

        new_stroke = TextStroke(event.x, event.y, self.line_style, self.color.get(
        ), self.width.get(), self.canvas, self.font.get(), self.font_size.get())
        self.strokes.append(new_stroke)
        self.curr_stroke = new_stroke
        self.text_index = 0
        self.create_outline_curr_text()

    def create_outline_curr_text(self):
        if not isinstance(self.curr_stroke, TextStroke):
            return
        if self.curr_text_rect:
            self.canvas.delete(self.curr_text_rect)
        bbox = self.canvas.bbox(self.curr_stroke.tk_painting[0])
        self.curr_text_rect = self.canvas.create_rectangle(
            bbox, outline="green", fill="black")
        self.canvas.tag_raise(
            self.curr_stroke.tk_painting[0], self.curr_text_rect)

    def handle_btn_release(self) -> None:
        if self.state.get() == State.TEXT.value:
            return
        if self.drag_strokes:
            self.drag_strokes = False
        if self.state.get() != State.SELECT.value and self.state.get() != State.POLYGON.value and self.curr_stroke:
            self.undo_actions = []
            self.actions.append(CreateAction(
                painter_strokes=self.strokes, strokes=[self.curr_stroke]))
            self.curr_stroke = None
        else:
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

        for stroke in self.strokes:
            if stroke in self.selected_strokes:
                continue
            if (isinstance(stroke, ShapeStroke) and stroke.shape.value == Shape.RECT.value) or (isinstance(stroke, TextStroke)):
                x1, y1, x2, y2 = self.canvas.bbox(stroke.tk_painting[0])
                if x1 > rect_range_x.stop or x2 < rect_range_x.start:
                    continue
                if y1 > rect_range_y.stop or rect_range_y.start > y2:
                    continue
                if isinstance(stroke, ShapeStroke) and not stroke.fill:
                    if x1 < rect_range_x.start and x2 > rect_range_x.stop and y1 < rect_range_y.start and y2 > rect_range_y.stop:
                        continue
            elif isinstance(stroke, PolygonStroke):
                coordinates = []
                for i, co in enumerate(stroke.coordinates):
                    if i:
                        coordinates += calculate_points_on_line(
                            *stroke.coordinates[i - 1], *co)
                if set(selected_rect).isdisjoint(coordinates):
                    continue
            elif isinstance(stroke, TriangleStroke):
                is_in = False
                for co in selected_rect:
                    if is_point_inside_triangle(co, stroke.coordinates[0], ((stroke.coordinates[0][0] + stroke.coordinates[1][0])//2, stroke.coordinates[1][1]), (stroke.coordinates[1][0], stroke.coordinates[0][1])):
                        is_in = True
                        break
                if not is_in:
                    continue
            elif isinstance(stroke, ShapeStroke) and stroke.shape.value == Shape.OVAL.value:
                is_in = False
                for co in selected_rect:
                    if is_point_inside_oval(co, stroke.coordinates[0], stroke.coordinates[1]):
                        is_in = True
                        break
                if not is_in:
                    continue
            elif set(selected_rect).isdisjoint(stroke.coordinates):
                continue

            group = next(
                (group for group in self.groups if stroke in group), None)

            if group:
                for s in group:
                    self.selected_strokes.append(s)
            else:
                self.selected_strokes.append(stroke)

        if not len(self.selected_strokes):
            return

        bbox = self.canvas.bbox(
            *[i for stroke in self.selected_strokes for i in stroke.tk_painting])
        self.selected_rect = self.canvas.create_rectangle(
            *bbox, outline="green")
        self.selected_rect_locs = bbox

    def try_to_delete(self, label):
        try:
            self.selected_menu.delete(label)
        except:
            pass

    def handle_right_click(self, event: tk.Event) -> None:
        if len(self.selected_strokes) > 0 and self.selected_rect_locs:
            if event.x > self.selected_rect_locs[0] and event.x < self.selected_rect_locs[2] and event.y > self.selected_rect_locs[1] and event.y < self.selected_rect_locs[3]:

                self.try_to_delete("Text Properties")
                self.try_to_delete("Shape Properties")
                self.try_to_delete("Ungroup")
                self.try_to_delete("Group")

                is_text = [isinstance(stroke, TextStroke)
                           for stroke in self.selected_strokes]

                if any(is_text):
                    if len(list(filter(lambda i: i, is_text))) == 1:
                        text_stroke = self.selected_strokes[is_text.index(True)]
                        if isinstance(text_stroke, TextStroke):
                            font = text_stroke.font
                            font_size = text_stroke.font_size
                            color = text_stroke.color
                        else:
                            font = ""
                            font_size = 14
                            color = ""
                    else:
                        font = ""
                        color = ""
                        font_size = 14

                    self.selected_menu.add_command(label="Text Properties", command=lambda:
                                                   TextOptions(self.root,
                                                               font=font,
                                                               font_size=font_size,
                                                               color=color,
                                                               on_save=self.on_save_text,
                                                               multiple=(len(list(filter(lambda stroke: isinstance(
                                                                   stroke, TextStroke), self.selected_strokes))) != 1)
                                                               ))

                if any([not i for i in is_text]):
                    if len(list(filter(lambda i: not i, is_text))) == 1:
                        shape_stroke = self.selected_strokes[is_text.index(False)]
                        print(shape_stroke.width)
                        if hasattr(shape_stroke, "fill"):
                                fill = shape_stroke.fill
                        else:
                            fill = self.fill.get()
                        color = shape_stroke.color
                        width = shape_stroke.width
                    else:
                        fill = self.fill.get()
                        color = self.color.get()
                        width = self.width.get()
                    self.selected_menu.add_command(label="Shape Properties", command=lambda:
                                                   ShapeOptions(self.root,
                                                                fill=fill,
                                                                color=color,
                                                                width=width,
                                                                on_save=self.on_save_shape,
                                                                multiple=(len(list(filter(lambda stroke: not isinstance(
                                                                    stroke, TextStroke), self.selected_strokes))) != 1)
                                                                ))
                if len(self.selected_strokes) > 1:
                    if frozenset(self.selected_strokes) in self.groups:
                        self.selected_menu.add_command(label="Ungroup", command=lambda: self.groups.remove(
                            frozenset(self.selected_strokes)))
                    else:
                        for group in self.groups.copy():
                            for stroke in self.selected_strokes:
                                if stroke in group:
                                    self.groups.remove(group)
                                    break
                        self.selected_menu.add_command(label="Group", command=lambda: self.groups.add(
                            frozenset(self.selected_strokes)))

                try:
                    self.selected_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    self.selected_menu.grab_release()
        else:
            self.paste_coordinates = (event.x, event.y)
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()

    def on_save_text(self, font: str, font_size: int, color: str) -> None:
        changed_strokes: List[Stroke] = []
        og_props: List[Dict[str, Any]] = []
        for text_stroke in filter(lambda stroke: isinstance(stroke, TextStroke), self.selected_strokes):
            if not isinstance(text_stroke, TextStroke):
                continue
            changed_strokes.append(text_stroke)
            og_props.append(
                {"font": text_stroke.font, "font_size": text_stroke.font_size, "color": text_stroke.color})
            fonts = load_available_fonts()
            if font in fonts:
                text_stroke.font = font
            else:
                text_stroke.font = "Arial"
            text_stroke.font_size = font_size
            if len(color):
                text_stroke.color = color
        self.undo_actions = []
        self.actions.append(ChangePropAction(
            painter_strokes=self.strokes, strokes=changed_strokes, og_props=og_props))
        for stroke in self.strokes:
            if stroke in self.selected_strokes and isinstance(stroke, TextStroke):
                stroke.paint()
            else:
                for i in stroke.tk_painting:
                    self.canvas.tag_raise(i)

    def on_save_shape(self, fill: str, color: str, width: int) -> None:
        changed_strokes: List[Stroke] = []
        og_props: List[Dict[str, Any]] = []
        for shape_stroke in filter(lambda stroke: not isinstance(stroke, TextStroke), self.selected_strokes):
            changed_strokes.append(shape_stroke)
            og_props.append({"color": shape_stroke.color,
                            "width": shape_stroke.width})

            if hasattr(shape_stroke, "fill"):
                og_props[-1]["fill"] = shape_stroke.fill
                shape_stroke.fill = fill
            shape_stroke.color = color

            shape_stroke.width = width
        self.undo_actions = []
        self.actions.append(ChangePropAction(
            painter_strokes=self.strokes, strokes=changed_strokes, og_props=og_props))
        for stroke in self.strokes:
            if stroke in self.selected_strokes and not isinstance(stroke, TextStroke):
                stroke.paint()
            else:
                for i in stroke.tk_painting:
                    self.canvas.tag_raise(i)

    def delete_selected(self) -> None:
        for stroke in self.selected_strokes:
            stroke.delete()
            self.strokes.remove(stroke)
        self.remove_select()

    def delete_all(self) -> None:
        self.actions.append(ClearCanvasAction(
            self.strokes, [i for i in self.strokes], self.canvas))
        self.canvas.delete("all")
        self.strokes = []
        self.selected_strokes = []

    def handle_typing(self, event) -> None:
        if not self.curr_stroke or not isinstance(self.curr_stroke, TextStroke) or not isinstance(self.text_index, int):
            return
        if event.keysym == 'BackSpace':
            if self.text_index <= 0:
                return
            self.curr_stroke.remove_char(self.text_index - 1)
            self.text_index -= 1
            self.create_outline_curr_text()
        elif event.keysym == "Left":
            if self.text_index <= 0:
                return
            self.text_index -= 1
        elif event.keysym == "Right":  
            if self.text_index >= len(self.curr_stroke.text):
                return
            self.text_index += 1
        elif event.char:
            self.curr_stroke.add_char(event.char, self.text_index)
            self.text_index += 1
            self.create_outline_curr_text()

    def save_to_json(self) -> None:
        strokes = [{
            "type": stroke.__class__.__name__,
            "coordinates": stroke.coordinates,
            "line_style": stroke.line_style.name,
            "color": stroke.color,
            "fill": stroke.fill if hasattr(stroke, "fill") else "",
            "width": stroke.width,
            "font": stroke.font if hasattr(stroke, "font") else "",
            "font_size": stroke.font_size if hasattr(stroke, "font_size") else "",
            "shape": stroke.shape.name if hasattr(stroke, "shape") else "",
            "text": stroke.text if hasattr(stroke, "text") else ""
        } for stroke in self.strokes]

        now = datetime.now()
        curr_date = now.strftime("%d%m%y-%H%M%S")

        with open("canvas-data-"+curr_date + ".json", "w") as json_file:
            json.dump(strokes, json_file, indent=4)

    def restore_data_from_json(self, filename) -> bool:
        try:
            json_data = open(filename)
            strokes = json.load(json_data)
            old_strokes = [i for i in self.strokes]
            self.canvas.delete("all")
            self.strokes = []
            self.selected_strokes = []

            for stroke in strokes:
                if stroke["type"] == "FreeStyleStroke":
                    s: Stroke = FreeStyleStroke(
                        0, 0, LineStyle[stroke["line_style"]], stroke["color"], stroke["width"], self.canvas)
                elif stroke["type"] == "PolygonStroke":
                    s = PolygonStroke(0, 0, LineStyle[stroke["line_style"]], stroke["color"], stroke["width"],
                                      self.canvas, fill=stroke["fill"], coordinates=[tuple(co) for co in stroke["coordinates"]]) # type: ignore
                elif stroke["type"] == "TextStroke":
                    s = TextStroke(stroke["coordinates"][0][0], stroke["coordinates"][0][1], line_style=LineStyle[stroke["line_style"]], color=stroke["color"],
                                   width=stroke["width"], canvas=self.canvas, font=stroke["font"], font_size=stroke["font_size"], text=stroke["text"])
                elif stroke["type"] == "ShapeStroke":
                    s = ShapeStroke(0, 0, LineStyle[stroke["line_style"]], stroke["color"],
                                    stroke["width"], self.canvas, fill=stroke["fill"], shape=Shape[stroke["shape"]])
                elif stroke["type"] == "TriangleStroke":
                    s = TriangleStroke(0, 0, LineStyle[stroke["line_style"]], stroke["color"],
                                       stroke["width"], self.canvas, fill=stroke["fill"], shape=Shape.TRIANGLE)
                
                s.coordinates = [tuple(co) for co in stroke["coordinates"]] # type: ignore
                s.paint()
                self.strokes.append(s)
            self.undo_actions = []
            self.actions.append(LoadJsonAction(self.strokes, old_strokes))
            return True
        except:
            return False

    def create_pil_img(self) -> None:
        img = Image.new("RGB", (self.canvas.winfo_width(),
                        self.canvas.winfo_height()), "black")
        draw = ImageDraw.Draw(img)

        for stroke in self.strokes:
            if isinstance(stroke, TriangleStroke):
                mid = (
                    stroke.coordinates[0][0] + stroke.coordinates[1][0])//2, stroke.coordinates[1][1]
                draw.polygon([*stroke.coordinates[0], *mid, stroke.coordinates[1][0], stroke.coordinates[0][1]],
                             fill=stroke.fill if len(stroke.fill) else None, outline=stroke.color, width=stroke.width)
            elif isinstance(stroke, PolygonStroke):
                draw.polygon(stroke.coordinates, fill=stroke.fill if len(
                    stroke.fill) else None, outline=stroke.color, width=stroke.width)
            elif isinstance(stroke, ShapeStroke):
                print("hih")
                coordinates = min(stroke.coordinates[0][0], stroke.coordinates[1][0]), min(stroke.coordinates[0][1], stroke.coordinates[1][1]), max(
                    stroke.coordinates[0][0], stroke.coordinates[1][0]), max(stroke.coordinates[0][1], stroke.coordinates[1][1])
                if stroke.shape.value == Shape.OVAL.value:
                    draw.ellipse(coordinates, outline=stroke.color, fill=stroke.fill if len(
                        stroke.fill) else None, width=stroke.width)
                else:
                    draw.rectangle(coordinates, outline=stroke.color, fill=stroke.fill if len(
                        stroke.fill) else None, width=stroke.width)
            elif isinstance(stroke, FreeStyleStroke):
                for i, co in enumerate(stroke.coordinates):
                    if i == 0:
                        continue
                    draw.line(
                        (*stroke.coordinates[i-1], *co), fill=stroke.color, width=stroke.width)
            elif isinstance(stroke, TextStroke):
                print(f"./assets/fonts/{stroke.font}.ttf")
                font = ImageFont.truetype(
                    f"./assets/fonts/{stroke.font}.ttf", int((stroke.font_size / 72) * 96))
                _, descent = font.getmetrics()
                text_width = font.getmask(stroke.text).getbbox()[2]
                print(text_width)
                text_height = font.getmask(stroke.text).getbbox()[3] + descent

                # Calculate the coordinates to center the text
                x = stroke.coordinates[0][0] - (text_width // 2)
                print(stroke.coordinates)
                print(stroke.coordinates[0][0], x)
                y = stroke.coordinates[0][1] - (text_height // 2)

                draw.text((x, y), stroke.text, fill=stroke.color, font=font)
        i = 1
        while True:
            if os.path.isfile(f"image{i}.png"):
                i += 1
            else:
                img.save(f"image{i}.png")
                break
