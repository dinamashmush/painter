from typing import *
from typing import *
from typing import List
from enums import *
from stroke import *
import tkinter as tk
from copy import copy
from stroke import  List, Stroke


class Action():
    """
    Base class for actions performed on strokes in the canvas.

    Attributes:
        painter_strokes (List[Stroke]): List of all strokes on the canvas. (pointer to the list the painter holds)
    """

    def __init__(self, painter_strokes: List[Stroke]) -> None:
        self.painter_strokes = painter_strokes
    
    def undo(self):
        """
        Undo the action.

        Returns:
            Action: The action that was undone.
        """
        pass
    def redo(self):
        """
        redo the action.

        Returns:
            Action: The action that was redone.
        """
        pass
    
class CreateAction(Action):
    """a create action
    """
    def __init__(self, painter_strokes: List[Stroke], strokes: List[Stroke]):
        super().__init__(painter_strokes)
        self.strokes = strokes
        
    def undo(self) -> Action:
        for stroke in self.strokes:
            self.painter_strokes.remove(stroke)
            stroke.delete()
        return CreateAction(strokes=self.strokes, painter_strokes=self.painter_strokes)
    
    def redo(self) -> Action:
        for stroke in self.strokes:
            self.painter_strokes.append(stroke)
            stroke.paint()
        return CreateAction(strokes=self.strokes, painter_strokes=self.painter_strokes)


class ChangePropAction(Action):
    """a change properties action.
    """
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
    """a change order of strokes action
    """
    def __init__(self, painter_strokes: List[Stroke], og_indexes:List[int], canvas:tk.Canvas) -> None:
        super().__init__(painter_strokes)
        self.og_indexes = og_indexes
        self.canvas = canvas
        
    def undo(self) -> Action:
        new_indexes = [self.og_indexes.index(i) for i, _ in enumerate(self.og_indexes)]
        self.copied_strokes = [i for i in self.painter_strokes]
        self.painter_strokes.sort(key=lambda stroke: self.og_indexes[self.copied_strokes.index(stroke)])
        for stroke in self.painter_strokes:
            for p in stroke.tk_painting:
                self.canvas.tag_raise(p)
            
        return ChangeOrderAction(self.painter_strokes, og_indexes=new_indexes, canvas=self.canvas)
    
    def redo(self) -> Action:
        return self.undo()
    

class ClearCanvasAction(Action):
    """clear canvas action
    """
    def __init__(self, painter_strokes: List[Stroke], strokes: List[Stroke], canvas:tk.Canvas) -> None:
        super().__init__(painter_strokes)
        self.canvas = canvas
        self.strokes = strokes
        
    def undo(self) -> Action:
        for stroke in self.strokes:
            self.painter_strokes.append(stroke)
            stroke.paint()
        return ClearCanvasAction(self.painter_strokes, self.strokes, self.canvas)
    
    def redo(self) -> Action:
        action =  ClearCanvasAction(self.painter_strokes, [i for i in self.painter_strokes], self.canvas)
        self.canvas.delete("all")
        self.painter_strokes.clear()
        return action

class LoadJsonAction(Action):
    """load data from json file action
    """
    def __init__(self, painter_strokes: List[Stroke], strokes: List[Stroke]) -> None:
        super().__init__(painter_strokes)
        self.strokes = strokes
    
    def undo(self) -> Action:
        old_strokes = copy(self.painter_strokes)
        for stroke in [i for i in self.painter_strokes]:
            stroke.delete()
            self.painter_strokes.remove(stroke)
        for stroke in self.strokes:
            self.painter_strokes.append(stroke)
            stroke.paint()
        return LoadJsonAction(self.painter_strokes, strokes=old_strokes)
    
    def redo(self):
        return self.undo()