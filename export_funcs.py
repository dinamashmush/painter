import tkinter as tk
import os.path
from PIL import ImageGrab
from canvasvg import saveall # type: ignore


def export_to_png(canvas: tk.Canvas, root) -> None:
    if is_partially_off_screen(root):
        error_popup(root, "to save as png, please make sure all of your window is visible and try again")
        return
    x = root.winfo_rootx() + 50
    y = root.winfo_rooty() + 30
    img = ImageGrab.grab()
    img = img.crop((x*1.5, y*1.5, (x + canvas.winfo_width())
                   * 1.5, (y + canvas.winfo_height())*1.5))

    i = 1
    while True:
        if os.path.isfile(f"image{i}.png"):
            i += 1
        else:
            img.save(f"image{i}.png")
            break


def export_to_svg(canvas: tk.Canvas, root) -> None:
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
    i = 1
    while True:
        if os.path.isfile(f"image{i}.eps"):
            i += 1
        else:
            canvas.postscript(file=f"image{i}.eps")
            break


def is_partially_off_screen(window):
    win_x = window.winfo_x()
    win_y = window.winfo_y()
    win_width = window.winfo_width()
    win_height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    return (win_x < 0 or
            win_y < 0 or
            win_x + win_width > screen_width or
            win_y + win_height > screen_height)


def error_popup(root, text) -> None:
        error_frame = tk.Toplevel(root)
        error_frame.title("error")
        error_message = tk.Label(error_frame, text=text)
        error_message.pack()
        error_btn = tk.Button(error_frame, text="okay",
                              command=lambda: error_frame.destroy())
        error_btn.pack()
