from typing import *
from enums import LineStyle
import tkinter as tk
import math

class Stroke():
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int, canvas: tk.Canvas) -> None:
        self.line_style = line_style
        self.color = color
        self.coordinates: List[Tuple[int, int]] = [(x, y)]
        self.width = width
        self.selected = False
        self.canvas = canvas
        self.lines: List[int] = []
        self.prev_x = x
        self.prev_y = y

    def continue_stroke(self, x: int, y: int) -> None:
        
        line = self.canvas.create_line(self.prev_x, self.prev_y,
                                        x, y,
                                        fill=self.color,
                                        width=self.width,
                                        smooth=True)
        # self.canvas.create_oval(x-2, y-2, x+2, y+2, outline="red")
        # line = self.canvas.create_oval(x-(self.width//2), y - self.width//2, x + self.width//2, y+self.width//2, fill=self.color, outline=self.color)
        self.lines.append(line)
        self.coordinates.append((x,y))
        # line_pixels = linewidthpixels(self.width, self.prev_x, self.prev_y, x, y)
        # for i in range(0, len(line_pixels), 2):
        #     self.coordinates.append((line_pixels[i], line_pixels[i+1]))
        # self.coordinates += line_pixels
        # for i in range(x-self.width//2, x+(self.width//2)+1):
        #     for j in range(y-self.width//2, y+(self.width//2)+1):
        #         if (x-i)**2 + (y-j)**2 <= (self.width/2):
        #             self.img.put(self.color, to=(i, j))      
        #             self.coordinates.append((i,j))
              
        # self.coordinates.append((x, y))
        # m1, b1 = find_graph(self.prev_x - self.width//2, self.prev_y, x, y - self.width//2)
        # m2, b2 = find_graph(self.prev_x + self.width//2, self.prev_y, x, y + self.width//2)
        # range_x = range(self.prev_x, x) if x>self.prev_x else range(x, self.prev_x)
        # range_y = range(self.prev_y, y) if y>self.prev_y else range(y, self.prev_y)
        # for i in range_x:
        #     for j in range_y:   
        #         d1 = distance_point(i, j, m1, b1)
        #         d2 = distance_point(i, j, m2, b2)
                
        #         if not (m1 !=0 and m2 != 0 and ((d1 < 0 and d2 < 0) or (d1 > 0 and d2 > 0))):
        #             self.img.put(self.color, to=(i, j))
        #             self.coordinates.append((i, j))
        self.prev_x = x
        self.prev_y = y

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
        
    def delete(self) -> None:
        for line in self.lines:
            self.canvas.delete(line)
    
    def paint(self) -> None:
        
        for i, co in enumerate(self.coordinates):
            if i == len(self.coordinates) - 1: return
            line = self.canvas.create_line(*co, *self.coordinates[i+1], fill=self.color, width=self.width,smooth=True)
            self.lines.append(line)

