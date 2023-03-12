import sys
import math

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
            
    # Triplet pythagoricien.
    # 3 - 4 - 5
    # 5 - 12 - 13
    # https://fr.wikipedia.org/wiki/Triplet_pythagoricien
    # Find the closest Pythagorean triple.
    # This creates a right triangle.
    # This is useful to assemble sheets on non-right angles.
    # They could be used to triangularize 3D spline curves.
    def Pythagore(self, x_pos, y_pos, x_number, y_number):
        x_iter = x_number
        y_iter = y_number
        # TODO: This is not a very good function.
        while True:
            print("Triangle : Trying x=", x_iter, "y=", y_iter)
            c_square = x_iter * x_iter + y_iter * y_iter
            c_number = int(math.sqrt(c_square))
            if c_number * c_number == c_square:
                break
            if (x_iter - x_number) / x_number > (y_iter - y_number) / y_number:
                y_iter += 1
            else:
                x_iter += 1
        print("Triangle : OK x=", x_iter, "y=", y_iter, "x=", c_number)
        self.Line(x_pos, y_pos, x_iter + 1, HOLES_RIGHT)
        self.Line(x_pos, y_pos, y_iter + 1, HOLES_DOWN)
        ratio = 1.0 / (c_number + 1.0)
        for c_index in range(1, c_number + 1):
            x_hole = x_pos + x_iter * c_index * ratio
            y_hole = y_pos + y_iter * (1.0 - c_index * ratio)
            self._holes.add((x_hole, y_hole))
            
    # TODO: Ajouter un flag pour des bords droits ou arrondis.
    def _DrawBorderSquare(self, the_output):
        x_end = self._x_size * mecano_step
        y_end = self._y_size * mecano_step

        draw_line_actual(the_output, 0, 0, 0, y_end, COLOR_BLACK)
        draw_line_actual(the_output, 0, y_end, x_end, y_end, COLOR_BLACK)
        draw_line_actual(the_output, x_end, y_end, x_end, 0, COLOR_BLACK)
        draw_line_actual(the_output, x_end, 0, 0, 0, COLOR_BLACK)

    def _DrawBorderRounded(self, the_output):
        half_step = mecano_step * 0.5
        x_end = self._x_size * mecano_step
        y_end = self._y_size * mecano_step
        x_end_half = x_end - half_step
        y_end_half = y_end - half_step

        draw_line_actual(the_output, 0, half_step, 0, y_end_half, COLOR_BLACK)
        draw_line_actual(the_output, half_step, y_end, x_end_half, y_end, COLOR_BLACK)
        draw_line_actual(the_output, x_end, y_end_half, x_end, half_step, COLOR_BLACK)
        draw_line_actual(the_output, x_end_half, 0, half_step, 0, COLOR_BLACK)

        right_angle = 90.0

        border_radius = mecano_step * 0.5
        draw_arc(the_output, half_step, half_step, border_radius, 2 * right_angle, 3 * right_angle, COLOR_BLACK)
        draw_arc(the_output, half_step, y_end_half, border_radius, right_angle, 2 * right_angle, COLOR_BLACK)
        draw_arc(the_output, x_end_half, y_end_half, border_radius, 0, right_angle, COLOR_BLACK)
        draw_arc(the_output, x_end_half, half_step, border_radius, 3 * right_angle, 0.0, COLOR_BLACK)

    def DrawDxf(self, the_output):
        init_output_fd(the_output)
        self._DrawBorderRounded(the_output)
        print("Number holes:", len(self._holes))
        for x_pos, y_pos in self._holes:
            draw_hole_actual(the_output, (0.5 + x_pos) * mecano_step, (0.5 + y_pos) * mecano_step, mecano_hole, COLOR_BLACK)
        exit_output_fd(the_output)


if __name__ == "__main__":
    # python .\meccano.py t_line.dxf 10 1 Line 0 0 10
    # python .\meccano.py t_rect.dxf 10 5 Rectangle 0 0 10 5
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
