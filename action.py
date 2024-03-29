from typing import *
from typing import *
from enums import *
from stroke import *
import tkinter as tk

from stroke import  Stroke


class Action():
    def __init__(self, painter_strokes: List[Stroke]) -> None:
        self.painter_strokes = painter_strokes
    
    def undo(self):
        pass
    def redo(self):
        pass
    
class CreateAction(Action):
    def __init__(self, painter_strokes: List[Stroke], stroke: Stroke):
        super().__init__(painter_strokes)
        self.stroke = stroke
        
    def undo(self) -> Action:
        self.painter_strokes.remove(self.stroke)
        self.stroke.delete()
        return CreateAction(stroke=self.stroke, painter_strokes=self.painter_strokes)
    
    def redo(self) -> Action:
        self.painter_strokes.append(self.stroke)
        self.stroke.paint()
        return CreateAction(stroke=self.stroke, painter_strokes=self.painter_strokes)


class ChangePropAction(Action):
    def __init__(self, painter_strokes: List[Stroke], strokes:List[Stroke], og_props: List[Dict[str, Any]]):
        super().__init__(painter_strokes)
        self.strokes = strokes
        self.og_props = og_props
        
    def undo(self) -> Action:
        new_props: List[Dict[str, Any]] = []
        for i, stroke in enumerate(self.strokes):
            new_props.append(dict())
            for prop in self.og_props[i]:
                if hasattr(stroke, prop):
                    new_props[i][prop] = getattr(stroke, prop)
                    setattr(stroke, prop,self.og_props[i][prop])
                    stroke.paint()
        return ChangePropAction(self.painter_strokes, strokes=self.strokes, og_props=new_props)
                    
    def redo(self) -> Action:
        return self.undo()

class ChangeOrderAction(Action):
    def __init__(self, painter_strokes: List[Stroke], og_indexes:List[int], canvas:tk.Canvas) -> None:
        super().__init__(painter_strokes)
        self.og_indexes = og_indexes
        self.canvas = canvas
        
    def undo(self) -> Action:
        new_indexes = [self.og_indexes[self.og_indexes.index(i)] for i, _ in enumerate(self.og_indexes)]
        self.copied_strokes = [i for i in self.painter_strokes]
        self.painter_strokes.sort(key=lambda stroke: self.og_indexes[self.copied_strokes.index(stroke)])
        for stroke in self.painter_strokes:
            for p in stroke.tk_painting:
                self.canvas.tag_raise(p)
            
        return ChangeOrderAction(self.painter_strokes, og_indexes=new_indexes, canvas=self.canvas)
    
    def redo(self) -> Action:
        return self.undo()
    
