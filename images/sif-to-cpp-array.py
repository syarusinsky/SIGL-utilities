# A simple script to turn a sif image file into an initialized array of bytes in the c standard

import sys
import os

this_dir = os.path.dirname( os.path.realpath("__file__") )

if len(sys.argv) == 1:
    print( "ERROR: you need to specify the name of the sif file to convert" )
    quit()
else:
    font_name = sys.argv[1]

# open files
try:
    sif_file = open( font_name + ".sif", 'rb' )
except IOError:
    print( "ERROR: font file could not be found" )
    quit()

cpp_array_file = open( font_name + ".h", 'a' )

# clear h file just in case there's one already there
cpp_array_file.truncate( 0 )

# create c array
cpp_array_file.write( "uint8_t " + font_name + "_data[] = { " );

sif_byte = sif_file.read( 1 )
while sif_byte:
    byte_string = format( int.from_bytes(sif_byte, "big"), '#010b')
    sif_byte = sif_file.read( 1 )
    if sif_byte:
        byte_string = byte_string + ", "
    cpp_array_file.write( byte_string )

cpp_array_file.write( " };" );

# close files
sif_file.close()
cpp_array_file.close()
