from typing import *
from enums import LineStyle, Shape
import tkinter as tk
import numpy as np

class Stroke():
    def __init__(self, x: int, y: int,  line_style: LineStyle, color: str, width: int, canvas: tk.Canvas) -> None:
        self.line_style = line_style
        self.color = color
        self.coordinates: List[Tuple[int, int]] = [(x, y)]
        self.width = width
        self.tk_painting: List[int] = []
        self.canvas = canvas

    def delete(self) -> None:
        for line in self.tk_painting:
            self.canvas.delete(line)
    
    def paint(self) -> None:
        pass
    
    def move(self, dx:int, dy:int) -> None:
        self.coordinates = [(co[0] + dx, co[1] + dy) for co in self.coordinates]
        self.paint()

    
    def continue_stroke(self, x: int, y: int) -> None:
        pass
    
    

class FreeStyleStroke(Stroke):
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int, canvas: tk.Canvas):
        super().__init__(x, y, line_style, color, width, canvas) 
        self.prev_x = x
        self.prev_y = y


    def paint(self):
        for line in self.tk_painting:
            self.canvas.delete(line)

        for i, co in enumerate(self.coordinates):
            if i == len(self.coordinates) - 1: return
            line = self.canvas.create_line(*co, *self.coordinates[i+1], fill=self.color, width=self.width)
            self.tk_painting.append(line)
            
    
    def continue_stroke(self, x: int, y: int) -> None:
        
        line = self.canvas.create_line(self.prev_x, self.prev_y,
                                        x, y,
                                        fill=self.color,
                                        width=self.width)
        # self.canvas.create_oval(x-2, y-2, x+2, y+2, outline="red")
        # line = self.canvas.create_oval(x-(self.width//2), y - self.width//2, x + self.width//2, y+self.width//2, fill=self.color, outline=self.color)
        self.tk_painting.append(line)
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
        
    def __copy__(self):
        stroke =  FreeStyleStroke(self.coordinates[0], self.coordinates[1], line_style=self.line_style, color=self.color, width=self.width, canvas=self.canvas)
        stroke.coordinates = self.coordinates
        return stroke


class ShapeStroke(Stroke):
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int, canvas: tk.Canvas, fill: str, shape:Shape):
        super().__init__(x, y, line_style, color, width, canvas)
        self.shape: Shape = shape
        self.fill = fill
        
    def continue_stroke(self, x: int, y: int) -> None:
        if len(self.tk_painting):
            self.canvas.delete(self.tk_painting[0])
        self.coordinates = [self.coordinates[0]]
        self.coordinates.append((x, y))
        self.paint()            
    
    def paint(self) -> None:
        if len(self.tk_painting):
            self.canvas.delete(self.tk_painting[0])
        if self.shape.value == Shape.OVAL.value:
            self.tk_painting = [self.canvas.create_oval( *self.coordinates[0],*self.coordinates[1], outline=self.color, width=self.width, fill=self.fill)]
        elif self.shape.value == Shape.RECT.value:
            self.tk_painting = [self.canvas.create_rectangle( *self.coordinates[0],*self.coordinates[1], outline=self.color, width=self.width, fill=self.fill)]
    
    def __copy__(self):
        stroke =  ShapeStroke(self.coordinates[0], self.coordinates[1], line_style=self.line_style, color=self.color, width=self.width, canvas=self.canvas, shape=self.shape, fill=self.fill,)
        stroke.coordinates = self.coordinates
        return stroke


class TextStroke(Stroke):
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int, canvas: tk.Canvas,font:str, font_size:int, text:str = ""):
        super().__init__(x, y, line_style, color, width, canvas)
        self.text: str = text
        self.font_size = font_size
        self.font = font
        self.paint()
    
    def add_char(self, char:str, index:int) -> None:
        self.text = self.text[:index]+char+self.text[index:]
        self.paint()
    
    def remove_char(self, index:int):

        self.text = self.text[:index] + self.text[index + 1:]
        self.paint()
        
    
    def paint(self) -> None:
        if len(self.tk_painting):
            self.canvas.delete(self.tk_painting[0])
        self.tk_painting = [self.canvas.create_text(*self.coordinates[0], text=self.text, fill=self.color, font=(self.font,self.font_size))]
            

    def __copy__(self):
        stroke =  TextStroke(*self.coordinates[0], line_style=self.line_style, color=self.color, width=self.width, canvas=self.canvas, text=self.text)
        return stroke

class PolygonStroke(Stroke):
    
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int, canvas: tk.Canvas,fill:str, coordinates: List[Tuple[int, int]]) -> None:
        super().__init__(x, y, line_style, color, width, canvas)
        self.coordinates = coordinates
        self.fill = fill
        
    
    def paint(self) -> None:
        if len(self.tk_painting):
            self.canvas.delete(self.tk_painting[0])
        self.tk_painting = [self.canvas.create_polygon(*self.coordinates,fill=self.fill, width=self.width, outline=self.color)]
    
    def __copy__(self):
        stroke = PolygonStroke(*self.coordinates[0], line_style=self.line_style, color=self.color, width=self.width, canvas=self.canvas, fill=self.fill, coordinates=self.coordinates)
        return stroke



class UnfinishedPolygonStroke(Stroke):
    
    def __init__(self, x: int, y: int, line_style: LineStyle, color: str, width: int, canvas: tk.Canvas, fill:str) -> None:
        self.fill = fill
        super().__init__(x, y, line_style, color, width, canvas)
    
    def continue_stroke(self, x: int, y: int) -> None:
        self.tk_painting.append(self.canvas.create_line(*self.coordinates[-1], x, y, fill=self.color, width=self.width))
        self.coordinates.append((x, y))
    
    def paint(self) -> None:
        for painting in self.tk_painting:
            self.canvas.delete(painting)
        self.tk_painting = []
            
        for i, co in enumerate(self.coordinates):
            if i != 0:
                self.tk_painting.append(self.canvas.create_line(*self.coordinates[i-1], co[0], co[1], fill=self.color, width=self.width))
    
    def finish(self) -> PolygonStroke:
        for painting in self.tk_painting:
            self.canvas.delete(painting)
        stroke = PolygonStroke(0, 0, self.line_style, self.color, self.width, self.canvas, self.fill, self.coordinates)
        stroke.paint()
        return stroke
        


class TriangleStroke(ShapeStroke):
    def continue_stroke(self, x: int, y: int) -> None:
        self.coordinates = [self.coordinates[0]] + [(x, y)]
        self.paint()
        
    
    def paint(self) -> None:
        for painting in self.tk_painting:
            self.canvas.delete(painting)
        self.tk_painting = []
            
        mid = (self.coordinates[0][0] + self.coordinates[1][0])//2, self.coordinates[1][1]
        self.tk_painting = [self.canvas.create_polygon([*self.coordinates[0], *mid, self.coordinates[1][0], self.coordinates[0][1]], outline=self.color, fill=self.fill, width=self.width)]

    

def calculate_oval_coords(x1, y1, x2, y2, num_points=100):
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    semi_major_axis = (x2 - x1) / 2
    semi_minor_axis = (y2 - y1) / 2

    t = np.linspace(0, 2*np.pi, num_points)
    x = center_x + semi_major_axis * np.cos(t)
    y = center_y + semi_minor_axis * np.sin(t)
    
    x = np.round(x).astype(int)
    y = np.round(y).astype(int)

    return list(zip(x, y))
