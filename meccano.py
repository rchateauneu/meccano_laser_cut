import sys

from dxflib import *

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
            raise Exception("Negative y_pos ", y_pos)
        if y_pos >= self._y_size:
            raise Exception("Too big y_pos ", y_pos)
        self._holes.add((x_pos, y_pos))
        #print("Adding", (x_pos, y_pos))

    def Line(self, x_pos, y_pos, number, direction = HOLES_RIGHT):
        print("x_pos=", x_pos, "y_pos=", y_pos, "number=", number)
        for index in range(number):
            print("Index=", index)
            self._AddHoles(x_pos, y_pos)
            if direction == HOLES_RIGHT:
                x_pos += 1
            elif direction == HOLES_LEFT:
                x_pos -= 1
            elif direction == HOLES_DOWN:
                y_pos += 1
            elif direction == HOLES_UP:
                y_pos -= 1
            else:
                raise Exception("Invalid direction", direction)
                
    def Rectangle(self, x_pos, y_pos, x_number, y_number):
        print("x_pos=", x_pos, "y_pos=", y_pos, "x_number=", x_number, "y_number=", y_number)
        for index in range(x_number):
            self.Line(x_pos, y_pos, y_number, HOLES_DOWN)
            x_pos += 1
                    
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
        print("Number holes:", len(self._holes))
        for x_pos, y_pos in self._holes:
            draw_hole_actual(the_output, (0.5 + x_pos) * mecano_step, (0.5 + y_pos) * mecano_step, mecano_hole, COLOR_BLACK)
        exit_output_fd(the_output)


if __name__ == "__main__":
    #  python .\meccano.py toto.dxf 20 20 Line 1 1 10
    filename = sys.argv[1]
    print("filename=", filename)
    if not filename.endswith(".dxf"):
        raise Exception("Invalid filename", filename)

    x_size = int(sys.argv[2])
    y_size = int(sys.argv[3])
    meccano = MeccanoPart(x_size, y_size)
    functionname = sys.argv[4]
    print("functionname=", functionname)
    function = getattr(meccano, functionname)
    #exit()
    fd = open(filename, "w");
    
    function( *[int(a) for a in sys.argv[5:]] )
    
    meccano.DrawDxf(fd)
    fd.close()
