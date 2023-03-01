# Fabriquer un fichier DXF pour un laser cutter CNC.
# https://people.bath.ac.uk/ps281/teaching/maths3c/2DPinned_07_WritingDXFs.pdf

# Meccano system dates back to 1901 and is designed to Imperial sizes ie 1/2 inch hole spacings
# Plain holes in all Meccano parts are all 4.1mm in diameter, and are spaced at 1/2" (12.7mm),
# with some modern parts having twice as many holes to give a 1/4" (6.3mm) spacing.
# Meccano axles are a running fit in the holes, and are 4.06mm in diameter.
# This is actually an old Imperial SWG (Standard Wire Gauge) size 8.
mecano_step = 12.7
mecano_hole = 2.05

HOLES_LEFT = 1
HOLES_RIGHT = 2
HOLES_UP = 3
HOLES_DOWN = 4

# Eliminates duplicates lines and holes.
cache_lines = None
cache_holes = None

from dxflib import *

def init_output(path_name):
    print("init_output", path_name)
    global cache_lines, cache_holes
    cache_lines = set()
    cache_holes = set()

    the_output = init_output_actual(path_name)
    return the_output


def draw_line(the_output, x_start, y_start, x_end, y_end):
    if (x_start, y_start, x_end, y_end) in cache_lines:
        return
    cache_lines.add((x_start, y_start, x_end, y_end))
    
    # Convert holes number in millimeters.
    draw_line_actual(the_output, x_start * mecano_step, y_start * mecano_step, x_end * mecano_step, y_end * mecano_step, COLOR_BLACK)


def draw_hole(the_output, x_pos, y_pos, hole_color):
    if (x_pos, y_pos) in cache_holes:
        return
    cache_holes.add((x_pos, y_pos))
    
    # Convert holes number in millimeters.
    draw_hole_actual(the_output, x_pos * mecano_step, y_pos * mecano_step, mecano_hole, hole_color)


def draw_holes_line(the_output, x_start, y_start, num_holes, x_step, y_step, hole_color):
    if num_holes < 0:
        num_holes = -num_holes
        x_step = -x_step
        y_step = -y_step
    x_start += x_step / 2.0
    y_start += y_step / 2.0
    print("num_holes=", num_holes)
    for index_holes in range(num_holes):
        draw_hole(the_output, x_start, y_start, hole_color)
        x_start += x_step
        y_start += y_step


# TODO : Specific color for holes, so they can be cut at the beginning,
# before the material is cut into pieces making it instable.
# Take into account a possible stop of the machine in the middle of execution.


def draw_line_with_holes(the_output, x_start, y_start, x_end, y_end, holes_position):
    print("draw_line_with_holes")
    draw_line(the_output, x_start, y_start, x_end, y_end)
    
    # colour=5=blue (2=yellow, 4=cyan), black=0
    if holes_position == HOLES_LEFT:
        draw_holes_line(the_output, x_start - 0.5, y_start, y_end - y_start, 0, 1, COLOR_BLACK)
    elif holes_position == HOLES_RIGHT:
        draw_holes_line(the_output, x_start + 0.5, y_start, y_end - y_start, 0, 1, COLOR_DARK_BLUE)
    elif holes_position == HOLES_UP:
        draw_holes_line(the_output, x_start, y_start + 0.5, x_end - x_start, 1, 0, COLOR_BLACK) # Magenta
    elif holes_position == HOLES_DOWN:
        draw_holes_line(the_output, x_start, y_start - 0.5, x_end - x_start, 1, 0, COLOR_LIGHT_BLUE)
    else:
        return


def draw_rectangle_with_holes(the_output, x_offset, y_offset, x_size, y_size):
    print("draw_rectangle", x_offset, y_offset, x_size, y_size)
    draw_line_with_holes(the_output, x_offset, y_offset, x_offset+x_size, y_offset, HOLES_UP)
    draw_line_with_holes(the_output, x_offset+x_size, y_offset, x_offset+x_size, y_offset+y_size, HOLES_LEFT)
    draw_line_with_holes(the_output, x_offset+x_size, y_offset+y_size, x_offset, y_offset+y_size, HOLES_DOWN)
    draw_line_with_holes(the_output, x_offset, y_offset+y_size, x_offset, y_offset, HOLES_RIGHT)


def draw_sheet_1_2():
    def draw_third_1_2(the_output, x_offset):
        draw_rectangle_with_holes(the_output, x_offset, 0, 25, 16)
        draw_rectangle_with_holes(the_output, x_offset, 16, 25, 10)
        draw_rectangle_with_holes(the_output, x_offset, 16+10, 25, 11)
        draw_rectangle_with_holes(the_output, x_offset, 16+10+11, 25, 10)

    the_output = init_output("sheet_1_2.dxf")
    draw_third_1_2(the_output, 0)
    draw_third_1_2(the_output, 25)
    draw_third_1_2(the_output, 25+25)
    exit_output(the_output)
    

def draw_sheet_3():
    def draw_third_3(the_output, x_offset):
        draw_rectangle_with_holes(the_output, x_offset, 0, 25, 16)
        draw_rectangle_with_holes(the_output, x_offset, 16, 25, 16)

    the_output = init_output("sheet_3.dxf")
    draw_third_3(the_output, 0)
    draw_third_3(the_output, 25)
    draw_third_3(the_output, 25+25)
    exit_output(the_output)


draw_sheet_1_2()
draw_sheet_3()
