def validate_width(P):
    if len(P)>1:
        return False
    if str.isdigit(P) or P == "":
        return True
    else:
        return False
    
def validate_font_size(P):
    if len(P)>2:
        return False
    if str.isdigit(P) or P == "":
        return True
    else:
        return False
