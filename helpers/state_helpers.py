def hex_to_decimal(hex_colour_string):
    return tuple(int(hex_colour_string.strip("#")[i:i+2], 16) for i in (0, 2, 4))