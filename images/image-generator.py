# A simple script to create small bitmap images in .sif format from png images

import sys
import os
import array
import pygame


file_bitmap = [] # the bitmap of the image

this_dir = os.path.dirname( os.path.realpath("__file__") )
image_path = ""
bitmap_format = ""
if len(sys.argv) == 1:
    print( "ERROR: you need to specify the png image" )
    quit()
elif len(sys.argv) == 2:
    print( "ERROR: you need to specify the format (rgb, rgba, monochrome)" )
    quit()
else:
    image_name = sys.argv[1]
    image_path = os.path.join( this_dir, image_name )

    bitmap_format = sys.argv[2]
    if bitmap_format != "rgb" and bitmap_format != "rgba" and bitmap_format != "monochrome":
        print( "ERROR: you need to specify a valid format (rgb, rgba, monochrome)" )
        quit()

    if bitmap_format == "rgb":
        bitmap_format = 0
    elif bitmap_format == "rgba":
        bitmap_format = 1
    elif bitmap_format == "monochrome":
        bitmap_format = 2

pygame.init()
pygame.display.set_mode( (1,1), pygame.NOFRAME )
image_file = pygame.image.load( image_path ).convert_alpha()

bitmap_width = image_file.get_width()
bitmap_height = image_file.get_height()

output_file_name = str(sys.argv[1]).split( ".", 1 )
output_file_name = output_file_name[0]

# open output file and write header ( format, width, height )
output_file = open( output_file_name + ".sif", 'wb' )
output_file.write( bitmap_format.to_bytes(1, byteorder='big', signed=False) )
output_file.write( bitmap_width.to_bytes(4, byteorder='big', signed=False) )
output_file.write( bitmap_height.to_bytes(4, byteorder='big', signed=False) )

# loop through pixel data and append each pixel/alpha combination to the file_bitmap
pixel_data = pygame.surfarray.array3d( image_file )
alpha_data = pygame.surfarray.array_alpha( image_file )
for color_column, alpha_column in zip(pixel_data, alpha_data):
    for pixel, alpha in zip(color_column, alpha_column):
        file_bitmap.append( [pixel[0], pixel[1], pixel[2], alpha] )

# these variables are only used for monochrome mode
byte_val = 0 # the value of the byte to write to the file
byte_num = 0 # the actual byte to write the bit to
byte_accumulator = 0

# iterate through each pixel row-by-row and write to file
for row in range(0, bitmap_height):
    for pixel in range(0, bitmap_width):
        pixel_vals = file_bitmap[(pixel * bitmap_height) + row]

        if bitmap_format == 2: # bitmap format is monochrome
            num_to_bitshift = 7 - byte_accumulator

            if (pixel_vals[0] > 0 or pixel_vals[1] > 0 or pixel_vals[2] > 0) and pixel_vals[3] != 0:
                byte_val = byte_val | (1 << num_to_bitshift)

            byte_accumulator = byte_accumulator + 1
            if byte_accumulator >= 8:
                # for pixel in range(0, 8):
                #     print( "PIXEL NUM: {} = {}     BYTE NUM: {}     BYTE VAL: {}".format((byte_num * 8) + pixel, (byte_val >> (7 - pixel)) & 1, byte_num, byte_val) )
                output_file.write( bytes([byte_val]) )
                byte_val = 0
                byte_num = byte_num + 1
                byte_accumulator = 0
        elif bitmap_format == 1: # bitmap format is rgba
            output_file.write( bytes([pixel_vals[0]]) ) # r
            output_file.write( bytes([pixel_vals[1]]) ) # g
            output_file.write( bytes([pixel_vals[2]]) ) # b
            output_file.write( bytes([pixel_vals[3]]) ) # a
            print( str(pixel_vals[0]) + ", " + str(pixel_vals[1]) + ", "  + str(pixel_vals[2]) + ", " + str(pixel_vals[3]) );
        elif bitmap_format == 0: # bitmap format is rgb
            output_file.write( bytes([pixel_vals[0]]) ) # r
            output_file.write( bytes([pixel_vals[1]]) ) # g
            output_file.write( bytes([pixel_vals[2]]) ) # b
            # print( str(pixel_vals[0]) + ", " + str(pixel_vals[1]) + ", "  + str(pixel_vals[2]) );

# if the bitmap format is monochrome and there are remaining bits, write them to the file in a last byte
if bitmap_format == 2 and byte_accumulator > 0:
    # print( "BYTE: {0} VALUE: {1:#010b}".format(byte_num, byte_val) )
    output_file.write( bytes([byte_val]) )
    byte_val = 0
    byte_num = byte_num + 1
    byte_accumulator = 0

output_file.close()
