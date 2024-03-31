import json

def load_available_fonts():
    """
    Load available fonts from a JSON file.

    Returns:
        List[str]: A list of available fonts.
    """
    json_fonts = open("assets/fonts.json")
    fonts = json.load(json_fonts)["fonts"]
    return fonts