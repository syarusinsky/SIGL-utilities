# A simple script to create small bitmap fonts in .sff format from png images

import sys
import os
import array
import pygame


file_header = [] # the header for the entire file, goes right before the bitmap of the characters
file_bitmap = [] # the bitmap of all characters

this_dir = os.path.dirname( os.path.realpath("__file__") )
font_dir = ""
if len(sys.argv) == 1:
    print( "ERROR: you need to specify the directory of the font" )
    quit()
else:
    font_name = sys.argv[1]
    font_dir = os.path.join( this_dir, font_name )

if os.path.isdir(font_dir):
    print( "Font Directory: {}".format(font_dir) )
else:
    print( "ERROR: font directory is invalid" )

font_file = open( font_name + ".sff", 'wb')

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 &@\`^:,$=!/>#[{(<-%.|+?\"]});'*~_"

char_index = 0
bitmap_char_width = 0
bitmap_width = 0
bitmap_height = 0
bitmap_byte_start = 7 # the byte at which the mapping of character to bitmap index begins

for char in characters:
    file_header.append( char )
    file_header.append( char_index )
    if char == " ":
        char_img_path = os.path.join( font_dir, "space" + ".png" )
    elif char == "&":
        char_img_path = os.path.join( font_dir, "ampersand" + ".png" )
    elif char == "@":
        char_img_path = os.path.join( font_dir, "at" + ".png" )
    elif char == "\\":
        char_img_path = os.path.join( font_dir, "backslash" + ".png" )
    elif char == "`":
        char_img_path = os.path.join( font_dir, "backtick" + ".png" )
    elif char == "^":
        char_img_path = os.path.join( font_dir, "carat" + ".png" )
    elif char == ":":
        char_img_path = os.path.join( font_dir, "colon" + ".png" )
    elif char == ",":
        char_img_path = os.path.join( font_dir, "comma" + ".png" )
    elif char == "$":
        char_img_path = os.path.join( font_dir, "dollarsign" + ".png" )
    elif char == "=":
        char_img_path = os.path.join( font_dir, "equals" + ".png" )
    elif char == "!":
        char_img_path = os.path.join( font_dir, "exclamation" + ".png" )
    elif char == "/":
        char_img_path = os.path.join( font_dir, "forwardslash" + ".png" )
    elif char == ">":
        char_img_path = os.path.join( font_dir, "greaterthan" + ".png" )
    elif char == "#":
        char_img_path = os.path.join( font_dir, "hash" + ".png" )
    elif char == "[":
        char_img_path = os.path.join( font_dir, "leftbracket" + ".png" )
    elif char == "{":
        char_img_path = os.path.join( font_dir, "leftcurlybracket" + ".png" )
    elif char == "(":
        char_img_path = os.path.join( font_dir, "leftparenthesis" + ".png" )
    elif char == "<":
        char_img_path = os.path.join( font_dir, "lessthan" + ".png" )
    elif char == "-":
        char_img_path = os.path.join( font_dir, "minus" + ".png" )
    elif char == "%":
        char_img_path = os.path.join( font_dir, "percent" + ".png" )
    elif char == ".":
        char_img_path = os.path.join( font_dir, "period" + ".png" )
    elif char == "|":
        char_img_path = os.path.join( font_dir, "pipe" + ".png" )
    elif char == "+":
        char_img_path = os.path.join( font_dir, "plus" + ".png" )
    elif char == "?":
        char_img_path = os.path.join( font_dir, "questionmark" + ".png" )
    elif char == "\"":
        char_img_path = os.path.join( font_dir, "quotes" + ".png" )
    elif char == "]":
        char_img_path = os.path.join( font_dir, "rightbracket" + ".png" )
    elif char == "}":
        char_img_path = os.path.join( font_dir, "rightcurlybracket" + ".png" )
    elif char == ")":
        char_img_path = os.path.join( font_dir, "rightparenthesis" + ".png" )
    elif char == ";":
        char_img_path = os.path.join( font_dir, "semicolon" + ".png" )
    elif char == "'":
        char_img_path = os.path.join( font_dir, "singlequotes" + ".png" )
    elif char == "*":
        char_img_path = os.path.join( font_dir, "star" + ".png" )
    elif char == "~":
        char_img_path = os.path.join( font_dir, "tilde" + ".png" )
    elif char == "_":
        char_img_path = os.path.join( font_dir, "underscore" + ".png" )
    else:
        char_img_path = os.path.join( font_dir, char + ".png" )
    char_img = pygame.image.load( char_img_path )
    bitmap_char_width = char_img.get_width()
    bitmap_width = bitmap_width + char_img.get_width() # individual widths may change in the future
    bitmap_height = char_img.get_height() # always a constant height
    bitmap_byte_start = bitmap_byte_start + 2 # plus 2 due to mapping of character to bitmap index

    pixel_data = pygame.surfarray.array3d( char_img )
    for column in pixel_data:
        for pixel in column:
            if pixel[0] != 0 and pixel[1] != 0 and pixel[2] != 0:
                file_bitmap.append( True )
            else:
                file_bitmap.append( False )

    char_index = char_index + 1

# get the bytes for bitmap width
bitmap_width_bytes = bitmap_width.to_bytes( 4, byteorder='big', signed=False )

# write character width (1 byte), width (4 bytes), height (1 byte), and bitmap byte start (1 byte)
font_file.write( bytes([bitmap_char_width]) )
font_file.write( bytes([bitmap_width_bytes[0]]) )
font_file.write( bytes([bitmap_width_bytes[1]]) )
font_file.write( bytes([bitmap_width_bytes[2]]) )
font_file.write( bytes([bitmap_width_bytes[3]]) )
font_file.write( bytes([bitmap_height]) )
font_file.write( bytes([bitmap_byte_start]) )

for byte in file_header:
    if isinstance( byte, str ):
        font_file.write( bytes(byte.encode('ascii')) )
    else:
        font_file.write( bytes([byte]) )

byte_val = 0 # the value of the byte to write to the file
byte_num = 0 # the actual byte to write the bit to
byte_accumulator = 0
for row in range(0, bitmap_height):
    for pixel in range(0, bitmap_width):
        num_to_bitshift = 7 - byte_accumulator

        if file_bitmap[(pixel * bitmap_height) + row] == True:
            byte_val = byte_val | (1 << num_to_bitshift)

        byte_accumulator = byte_accumulator + 1
        if byte_accumulator >= 8:
            # for bit in range(0, 8):
                # print( "PIXEL NUM: {} = {}     BYTE NUM: {}".format((byte_num * 8) + bit, (byte_val >> (7 - bit)) & 1, byte_num) )
            font_file.write( bytes([byte_val]) )
            byte_val = 0
            byte_num = byte_num + 1
            byte_accumulator = 0

if byte_accumulator > 0:
    # print( "BYTE: {0} VALUE: {1:#010b}".format(byte_num, byte_val) )
    font_file.write( bytes([byte_val]) )
    byte_val = 0
    byte_num = byte_num + 1
    byte_accumulator = 0

font_file.close()
