def validate_width(P: str) -> bool:
    """Validate the input for line width.
    returns True if P is a digit between 1 and 9, False otherwise
    """
    if len(P)>1:
        return False
    if P == "0":
        return False
    if str.isdigit(P):
        return True
    else:
        return False
    
def validate_font_size(P: str) -> bool:
    """Validate the input for font size.
    returns True if P is a 1 or 2 digit number or empty, False otherwise
    """
    if len(P)>2:
        return False
    if P == "0":
        return False
    if str.isdigit(P) or P == "":
        return True
    else:
        return False
