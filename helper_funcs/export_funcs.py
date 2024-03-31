import tkinter as tk
import os.path
from canvasvg import saveall # type: ignore
from typing import * 



def export_to_svg(canvas: tk.Canvas, root: tk.Misc) -> None:
    """
    Export the canvas to SVG format.

    Args:
        canvas (tk.Canvas): The canvas to export.
        root: The root window.
    """
    try:
        iter(canvas.bbox("all"))
    except TypeError:
        error_popup(root, "You cannot export an empty canvas to svg")
        return

    i = 1
    while True:
        if os.path.isfile(f"image{i}.svg"):
            i += 1
        else:
            saveall(f"image{i}.svg", canvas)
            break
        
        


def export_to_eps(canvas: tk.Canvas) -> None:
    """
    Export the canvas to EPS format.

    Args:
        canvas (tk.Canvas): The canvas to export.
    """

    i = 1
    while True:
        if os.path.isfile(f"image{i}.eps"):
            i += 1
        else:
            canvas.postscript(file=f"image{i}.eps")
            break


def error_popup(root: tk.Misc, text: str) -> None:
        """
        Display an error popup window.

        Args:
            root: The root window.
            text (str): The error message.
        """

        error_frame = tk.Toplevel(root)
        error_frame.grab_set()
        
        error_frame.title("error")
        error_message = tk.Label(error_frame, text=text)
        error_message.pack()
        error_btn = tk.Button(error_frame, text="okay",
                              command=lambda: error_frame.destroy())
        error_btn.pack()
