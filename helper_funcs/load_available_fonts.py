import json

def load_available_fonts():
    json_fonts = open("assets/fonts.json")
    fonts = json.load(json_fonts)["fonts"]
    return fonts