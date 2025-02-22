import tkinter as tk
from typing import *
class Tooltip:
    """a tooltip
    """
    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tooltip: Union[tk.Toplevel, None] = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event:Union[tk.Event, None] = None) -> None:
        x, y, _, _ = self.widget.bbox("insert") #type: ignore
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x-150}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event:Union[tk.Event, None] = None) -> None:
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

