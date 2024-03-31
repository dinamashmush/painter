from typing import *
from enums import Shape
import tkinter as tk

class Stroke():
    """
    Abstract base class representing a stroke.

    Attributes:
        color (str): The color of the stroke.
        coordinates (List[Tuple[int, int]]): The coordinates of the stroke.
        width (int): The width of the stroke.
        tk_painting (List[int]): The Tkinter IDs of the drawn elements.
        canvas (tk.Canvas): The canvas on which the stroke is drawn.
    """

    def __init__(self, x: int, y: int, color: str, width: int, canvas: tk.Canvas) -> None:
        self.color = color
        self.coordinates: List[Tuple[int, int]] = [(x, y)]
        self.width = width
        self.tk_painting: List[int] = []
        self.canvas = canvas

    def delete(self) -> None:
        """Deletes the stroke from the canvas."""
        for line in self.tk_painting:
            self.canvas.delete(line)
    
    def paint(self) -> None:
        """Paints the stroke on the canvas."""
        pass
    
    def move(self, dx:int, dy:int) -> None:
        """Moves the stroke by the specified offset."""
        self.coordinates = [(co[0] + dx, co[1] + dy) for co in self.coordinates]
        self.paint()

    
    def continue_stroke(self, x: int, y: int) -> None:
        """Continues the stroke."""
        pass
    
    

class FreeStyleStroke(Stroke):
    """a freestyle stroke
    """
    def __init__(self, x: int, y: int, color: str, width: int, canvas: tk.Canvas):
        super().__init__(x, y, color, width, canvas) 
        self.prev_x = x
        self.prev_y = y


    def paint(self):
        
        self.delete()
        
        for i, co in enumerate(self.coordinates):
            if i == len(self.coordinates) - 1: return
            line = self.canvas.create_line(*co, *self.coordinates[i+1], fill=self.color, width=self.width)
            self.tk_painting.append(line)
            
    
    def continue_stroke(self, x: int, y: int) -> None:
        
        line = self.canvas.create_line(self.prev_x, self.prev_y,
                                        x, y,
                                        fill=self.color,
                                        width=self.width)
        self.tk_painting.append(line)
        self.coordinates.append((x,y))
        self.prev_x = x
        self.prev_y = y
        
    def __copy__(self):
        stroke =  FreeStyleStroke(self.coordinates[0], self.coordinates[1], color=self.color, width=self.width, canvas=self.canvas)
        stroke.coordinates = self.coordinates
        return stroke


class ShapeStroke(Stroke):
    """a shape stroke - rectangle or oval
    """
    def __init__(self, x: int, y: int, color: str, width: int, canvas: tk.Canvas, fill: str, shape:Shape):
        super().__init__(x, y, color, width, canvas)
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
        stroke =  ShapeStroke(self.coordinates[0], self.coordinates[1], color=self.color, width=self.width, canvas=self.canvas, shape=self.shape, fill=self.fill,)
        stroke.coordinates = self.coordinates
        return stroke


class TextStroke(Stroke):
    """a text stroke
    """
    def __init__(self, x: int, y: int, color: str, width: int, canvas: tk.Canvas,font:str, font_size:int, bold:bool, italic:bool, text:str = ""):
        super().__init__(x, y, color, width, canvas)
        self.text: str = text
        self.font_size = font_size
        self.font = font
        self.bold = bold
        self.italic = italic
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
        font = [self.font,self.font_size]
        if self.bold:
            font.append("bold")
        if self.italic:
            font.append("italic")
        self.tk_painting = [self.canvas.create_text(*self.coordinates[0], text=self.text, fill=self.color, font=font)]
            

    def __copy__(self):
        stroke = TextStroke(*self.coordinates[0], color=self.color, width=self.width, canvas=self.canvas, text=self.text, bold=self.bold, italic=self.italic, font=self.font, font_size=self.font_size)
        stroke.delete()
        stroke.tk_painting = []
        return stroke

class PolygonStroke(Stroke):
    """a polygon stroke
    """
    def __init__(self, x: int, y: int, color: str, width: int, canvas: tk.Canvas,fill:str, coordinates: List[Tuple[int, int]]) -> None:
        super().__init__(x, y, color, width, canvas)
        self.coordinates = coordinates
        self.fill = fill
        
    
    def paint(self) -> None:
        if len(self.tk_painting):
            self.canvas.delete(self.tk_painting[0])
        self.tk_painting = [self.canvas.create_polygon(*self.coordinates,fill=self.fill, width=self.width, outline=self.color)]
    
    def __copy__(self):
        stroke = PolygonStroke(*self.coordinates[0], color=self.color, width=self.width, canvas=self.canvas, fill=self.fill, coordinates=self.coordinates)
        return stroke



class UnfinishedPolygonStroke(Stroke):
    """an unfinished polygon - used only to create a polygon stroke.
    """
    
    def __init__(self, x: int, y: int, color: str, width: int, canvas: tk.Canvas, fill:str) -> None:
        self.fill = fill
        super().__init__(x, y, color, width, canvas)
    
    def continue_stroke(self, x: int, y: int) -> None:
        self.tk_painting.append(self.canvas.create_line(*self.coordinates[-1], x, y, fill=self.color, width=self.width))
        self.coordinates.append((x, y))
    
    def paint(self) -> None:
        self.delete()
        self.tk_painting = []
            
        for i, co in enumerate(self.coordinates):
            if i != 0:
                self.tk_painting.append(self.canvas.create_line(*self.coordinates[i-1], co[0], co[1], fill=self.color, width=self.width))
    
    def finish(self) -> PolygonStroke:
        for painting in self.tk_painting:
            self.canvas.delete(painting)
        stroke = PolygonStroke(0, 0, self.color, self.width, self.canvas, self.fill, self.coordinates)
        stroke.paint()
        return stroke
        


class TriangleStroke(ShapeStroke):
    """a triangle stroke
    """
    def continue_stroke(self, x: int, y: int) -> None:
        self.coordinates = [self.coordinates[0]] + [(x, y)]
        self.paint()
        
    
    def paint(self) -> None:
        for painting in self.tk_painting:
            self.canvas.delete(painting)
        self.tk_painting = []
            
        mid = (self.coordinates[0][0] + self.coordinates[1][0])//2, self.coordinates[1][1]
        self.tk_painting = [self.canvas.create_polygon([*self.coordinates[0], *mid, self.coordinates[1][0], self.coordinates[0][1]], outline=self.color, fill=self.fill, width=self.width)]
   
    def __copy__(self):
        stroke = TriangleStroke(*self.coordinates[0], color=self.color, width=self.width, canvas=self.canvas, fill=self.fill, shape=Shape.TRIANGLE)
        stroke.coordinates = self.coordinates
        return stroke
