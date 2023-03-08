import sys

from dxflib *

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
        
    def _AddHoles(self, x_pos, y_pos):
        if x_pos < 0:
            raise Exception("Negative x_pos ", x_pos)
        if x_pos >= self._x_size:
            raise Exception("Too big x_pos ", x_pos)
        if y_pos < 0:
            raise Exception("Negative x_pos ", x_pos)
        if y_pos >= self._y_size:
            raise Exception("Too big y_pos ", y_pos)

    def Line(self, x_pos, y_pos, number, direction = HOLES_RIGHT):
        for index in range(number):
            self._AddHoles(x_pos, y_pos)
            if direction == HOLES_RIGHT:
                ++x_pos
            elif direction == HOLES_LEFT:
                -x_pos
            elif direction == HOLES_DOWN:
                ++y_pos
            elif direction == HOLES_UP:
                --y_pos
            else:
                raise Exception("Invalid direction", direction)
                
    def Rectanlge(self, x_pos, y_pos, x_number, y_number):
        for index in range(x_number):
            self.Line(x_pos, y_pos, y_number, HOLES_RIGHT)
            ++x_pos
                    
    def _DrawBorder(self, the_output):
        x_end = self._x_size * mecano_step
        y_end = self._y_size * mecano_step
        draw_line_actual(the_output, 0, 0, 0, y_end, COLOR_BLACK)
        draw_line_actual(the_output, 0, y_end, x_end, y_end, COLOR_BLACK)
        draw_line_actual(the_output, x_end, y_end, x_end, 0, COLOR_BLACK)
        draw_line_actual(the_output, x_end, 0, 0, 0, COLOR_BLACK)

    def DrawDxf(self, the_output):
        init_output_fd(the_output)
        self._DrawBorder(the_output)
        for x_pos, y_pos in self._holes:
            draw_hole_actual(the_output, x_pos * mecano_step, y_pos * mecano_step, mecano_hole, COLOR_BLACK)
        exit_output_fd(the_output)


if __name__ == "__main__":
    filename = sys.argv[1]
    if not filename.endswith(".dxf"):
        raise Exception("Invalid filename", filename)

    x_size = int(sys.argv[1])
    y_size = int(sys.argv[2])
    meccano = MeccanoPart(x_size, y_size)
    functionname = sys.argv[2]
    function = getattr(meccano, functionname)
    fd = open(filename, "w");
    
    function(*sys.argv[2,])
    fd.close()
