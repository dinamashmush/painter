import tkinter as tk
from stroke import *
from enums import *

def test_text_stroke():
    # Create a Tkinter window for testing
    root = tk.Tk()
    canvas = tk.Canvas(root, width=200, height=200)
    canvas.pack()

    # Instantiate a TextStroke object
    text_stroke = TextStroke(50, 50, LineStyle.SOLID, "black", 1, canvas, text="Hello")

    # Test painting
    assert len(text_stroke.tk_painting) == 1, "TextStroke painting not created"
    assert text_stroke.text == "Hello", "TextStroke text not initialized correctly"

    # Test moving
    text_stroke.move(10, 10)
    assert text_stroke.coordinates == [(60, 60)], "TextStroke not moved correctly"
    
    # Test adding characters
    text_stroke.add_char("!", 5)
    assert text_stroke.text == "Hello!", "Character not added correctly"
    assert len(text_stroke.tk_painting) == 1, "TextStroke painting not updated after adding character"

    # Test removing characters
    text_stroke.remove_char(5)
    assert text_stroke.text == "Hello", "Character not removed correctly"
    assert len(text_stroke.tk_painting) == 1, "TextStroke painting not updated after removing character"

    # Cleanup
    canvas.delete("all")
    root.destroy()

def test_shape_stroke():
    
    # Create a Tkinter window for testing
    root = tk.Tk()
    canvas = tk.Canvas(root, width=200, height=200)
    canvas.pack()

    # Instantiate a ShapeStroke object (e.g., Oval)
    oval_stroke = ShapeStroke(50, 50, LineStyle.SOLID, "black", 1, canvas, fill="red", shape=Shape.OVAL)

    # Test updating coordinates on end for oval
    oval_stroke.continue_stroke(100, 100)
    assert len(oval_stroke.coordinates) == 2, "Oval ShapeStroke coordinates not updated correctly"

    # Test painting of oval
    oval_stroke.paint()
    assert len(oval_stroke.tk_painting) == 1, "Oval ShapeStroke painting not created"

    # Test moving oval
    oval_stroke.move(10, 10)
    assert oval_stroke.coordinates == [(60, 60), (110, 110)], "Oval ShapeStroke not moved correctly"

    # Instantiate a ShapeStroke object (e.g., Rectangle)
    rect_stroke = ShapeStroke(100, 100, LineStyle.SOLID, "blue", 1, canvas, fill="green", shape=Shape.RECT)

    # Test updating coordinates on end for rectangle
    rect_stroke.continue_stroke(150, 150)
    assert len(rect_stroke.coordinates) == 2, "Rectangle ShapeStroke coordinates not updated correctly"

    # Test painting of rectangle
    rect_stroke.paint()
    assert len(rect_stroke.tk_painting) == 1, "Rectangle ShapeStroke painting not created"

    # Test moving rectangle
    rect_stroke.move(-10, -10)
    assert rect_stroke.coordinates == [(90, 90), (140, 140)], "Rectangle ShapeStroke not moved correctly"

    # Test updating coordinates on end for rectangle after move
    rect_stroke.continue_stroke(160, 160)
    assert len(rect_stroke.coordinates) == 2, "Rectangle ShapeStroke coordinates not updated correctly after move"

    # Test updating coordinates on end for rectangle after move
    rect_stroke.update_coordinates_on_end()
    assert len(rect_stroke.coordinates) == 2, "Rectangle ShapeStroke coordinates not updated correctly on end after move"

    # Cleanup
    canvas.delete("all")
    root.destroy()

def test_free_style_stroke():
    # Create a Tkinter window for testing
    root = tk.Tk()
    canvas = tk.Canvas(root, width=200, height=200)
    canvas.pack()

    # Instantiate a FreeStyleStroke object
    free_style_stroke = FreeStyleStroke(50, 50, LineStyle.SOLID, "black", 1, canvas)

    # Test painting
    free_style_stroke.coordinates = [(50, 50), (100, 100), (150, 50)]
    free_style_stroke.paint()
    assert len(free_style_stroke.tk_painting) == 2, "FreeStyleStroke painting not created correctly"

    # Test moving
    free_style_stroke.move(10, 10)
    assert free_style_stroke.coordinates == [(60, 60), (110, 110), (160, 60)], "FreeStyleStroke not moved correctly"

    # Test continuing stroke
    free_style_stroke.continue_stroke(150, 150)
    assert len(free_style_stroke.coordinates) == 4, "FreeStyleStroke coordinates not updated correctly after continuing stroke"

    # Test copying stroke
    copied_stroke = free_style_stroke.__copy__()
    assert copied_stroke.coordinates == free_style_stroke.coordinates, "Copied stroke coordinates not matching"

    # Cleanup
    canvas.delete("all")
    root.destroy()


def test_polygon_stroke():
    # Create a Tkinter window for testing
    root = tk.Tk()
    canvas = tk.Canvas(root, width=200, height=200)
    canvas.pack()

    # Instantiate a PolygonStroke object
    polygon_stroke = PolygonStroke(50, 50, LineStyle.SOLID, "black", 1, canvas)

    # Test continuing the stroke
    polygon_stroke.continue_stroke(100, 100)
    assert len(polygon_stroke.coordinates) == 2, "PolygonStroke coordinates not updated correctly"

    # Test painting the polygon
    polygon_stroke.paint()
    assert len(polygon_stroke.tk_painting) == 1, "PolygonStroke painting not created"

    # Test moving the polygon
    polygon_stroke.move(10, 10)
    assert polygon_stroke.coordinates == [(60, 60), (110, 110)], "PolygonStroke not moved correctly"

    # Test continuing the stroke again
    polygon_stroke.continue_stroke(150, 50)
    assert len(polygon_stroke.coordinates) == 3, "PolygonStroke coordinates not updated correctly after continuing stroke"

    # Test painting the updated polygon
    polygon_stroke.paint()
    assert len(polygon_stroke.tk_painting) == 2, "Updated PolygonStroke painting not created"

    # Test moving the polygon again
    polygon_stroke.move(-20, 20)
    assert polygon_stroke.coordinates == [(40, 80), (90, 130), (130, 70)], "Updated PolygonStroke not moved correctly"

    # Cleanup
    canvas.delete("all")
    root.destroy()
    
    
def test_calculate_oval_coords():
    x1, y1, x2, y2 = 50, 50, 150, 100
    coords = calculate_oval_coords(x1, y1, x2, y2)
    assert len(coords) == 100, "Number of calculated points is incorrect"
    assert all([isinstance(coord, tuple) and len(coord) == 2 for coord in coords]), "Coordinates format is incorrect"

    x1, y1, x2, y2 = 0, 0, 100, 100
    coords = calculate_oval_coords(x1, y1, x2, y2)
    assert len(coords) == 100, "Number of calculated points is incorrect"
    assert all(isinstance(coord, tuple) and len(coord) == 2 for coord in coords), "Coordinates format is incorrect"

