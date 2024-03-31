import json
from typing import *

def load_available_fonts() -> List[str]:
    """
    Load available fonts from a JSON file.

    Returns:
        List[str]: A list of available fonts.
    """
    json_fonts = open("assets/fonts.json")
    fonts: List[str] = json.load(json_fonts)["fonts"]
    return fonts