from typing import *
from enums import LineStyle
import tkinter as tk

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
                line = self.canvas.create_line(*new_coordinates[i-1], x, y, fill=self.color, width=self.width,smooth=True)
                self.lines.append(line)
            new_coordinates.append((x, y))
        
        self.coordinates = new_coordinates
