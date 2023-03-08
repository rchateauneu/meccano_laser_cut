import sys

import dxflib

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

class MeccanoPart:
    def __init__(self, x_size, y_size):
        self._holes = set()
        self._x_size = x_size
        self._y_size = y_size
        
    def _AddHoles(solf, x_pos, y_pos):
        if x_pos < 0:
            raise Exception("Negative x_pos ", x_pos)
        if x_pos >= self._x_size:
            raise Exception("Too big x_pos ", x_pos)
        if y_pos < 0:
            raise Exception("Negative x_pos ", x_pos)
        if y_pos >= self._y_size:
            raise Exception("Too big y_pos ", y_pos)

    def Line(self, x_start, y_start, number):
    
    def _DrawBorder(self):
        x_end = self._x_size * 
    draw_line_actual(the_output, x_start, y_start, x_end, y_end, line_color)
    
    
    def DrawDxf(self, the_output):
init_output_fd(the_output):

        for index in range(number):
def draw_hole_actual(the_output, x_pos, y_pos, hole_diameter, hole_color):
            dxflib.draw_hole_actual()

exit_output_fd(the_output)

if __name__

