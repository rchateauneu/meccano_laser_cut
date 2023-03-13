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

# TODO : Create a part from a bitmap where each black pixel indicates a hole.


def _DrawBorderSquare(the_output, x_size, y_size):
    x_end = x_size * mecano_step
    y_end = y_size * mecano_step

    draw_line_actual(the_output, 0, 0, 0, y_end, COLOR_BLACK)
    draw_line_actual(the_output, 0, y_end, x_end, y_end, COLOR_BLACK)
    draw_line_actual(the_output, x_end, y_end, x_end, 0, COLOR_BLACK)
    draw_line_actual(the_output, x_end, 0, 0, 0, COLOR_BLACK)

def _DrawBorderRounded(the_output, x_size, y_size):
    half_step = mecano_step * 0.5
    x_end = x_size * mecano_step
    y_end = y_size * mecano_step
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

def _DrawBorder(the_output, x_size, y_size):
    # TODO: Ajouter un flag pour des bords droits ou arrondis.
    _DrawBorderRounded(the_output, x_size, y_size)


def _DrawBorderTriangle(the_output, x_size, y_size, c_number):
    border_radius = mecano_step * 0.5
    x_end = x_size * mecano_step
    y_end = y_size * mecano_step
    x_end_half = x_end - border_radius
    y_end_half = y_end - border_radius
    # Between 0 degrees (if y is small, horizontal triangle) and 90 degrees (if x small, vertical triangle)
    
    angle_radian = math.atan( (y_size-1) / (x_size-1))
    angle_degree = angle_radian * 180.0 / 3.14159
    print("angle_degree=", angle_degree, "c_number=", c_number)

    draw_line_actual(the_output, 0, border_radius, 0, y_end_half, COLOR_BLACK)
    draw_line_actual(the_output, x_end_half, 0, border_radius, 0, COLOR_BLACK)

    x_top_diagonal = border_radius + border_radius * math.sin(angle_radian)
    y_top_diagonal = y_end_half + border_radius * math.cos(angle_radian)
    x_bottom_diagonal = x_end_half + border_radius * math.sin(angle_radian)
    y_bottom_diagonal = border_radius + border_radius * math.cos(angle_radian)

    draw_line_actual(the_output, x_top_diagonal, y_top_diagonal, x_bottom_diagonal, y_bottom_diagonal, COLOR_BLACK)

    right_angle = 90.0

    draw_arc(the_output, border_radius, border_radius, border_radius, 2 * right_angle, 3 * right_angle, COLOR_BLACK)

    angle_top = right_angle - angle_degree
    draw_arc(the_output, border_radius, y_end_half, border_radius, angle_top, 2 * right_angle, COLOR_BLACK)
    angle_right = right_angle - angle_degree
    draw_arc(the_output, x_end_half, border_radius, border_radius, 3 * right_angle, angle_right, COLOR_BLACK)

    # BEWARE: The diagonal line of holes does not fit with vertical and horizontal holes.
    x_hole_diag_top = border_radius
    y_hole_diag_top = y_end_half
    x_diagonal_step = mecano_step * math.cos(angle_radian)
    y_diagonal_step = mecano_step * math.sin(angle_radian)

    for index in range(1, c_number):
        x_hole = x_hole_diag_top + x_diagonal_step * index
        y_hole = y_hole_diag_top - y_diagonal_step * index
        draw_hole_actual(the_output, x_hole, y_hole, mecano_hole, COLOR_BLACK)


class MeccanoPart:
    def __init__(self, file_output):
        self._holes = set()
        self._file_output = file_output
        init_output_fd(self._file_output)
        
    def Exit(self):
        exit_output_fd(self._file_output)
        
    def DrawDxf(self):
        print("Number holes:", len(self._holes))
        for x_pos, y_pos in self._holes:
            draw_hole_actual(self._file_output, (0.5 + x_pos) * mecano_step, (0.5 + y_pos) * mecano_step, mecano_hole, COLOR_BLACK)
        

    class ObjectTracer:
        def __init__(self, meccano, x_org, y_org):
            # So the origin is assumed to be zero.
            self._meccano = meccano
            print("x_org=", x_org, "y_org=", y_org)
            self._x_org = x_org
            self._y_org = y_org

        def _AddHoles(self, x_pos, y_pos):
            if x_pos < 0:
                raise Exception("Negative x_pos ", x_pos)
            if y_pos < 0:
                raise Exception("Negative y_pos ", y_pos)
            self._meccano._holes.add((self._x_org + x_pos, self._y_org + y_pos))

        def Line(self, number, direction = HOLES_RIGHT):
            x_pos, y_pos = 0, 0
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

            def LineBoundary(the_output):
                if direction in (HOLES_RIGHT, HOLES_LEFT):
                    _DrawBorder(the_output, number, 1)
                elif direction in (HOLES_DOWN, HOLES_UP):
                    _DrawBorder(the_output, 1, number)
                else:
                    raise Exception("Invalid direction", direction)
            return LineBoundary
                    
        def Rectangle(self, x_number, y_number):
            print("x_number=", x_number, "y_number=", y_number)
            x_pos = 0
            for index in range(x_number):
                y_pos = 0
                for index in range(y_number):
                    self._AddHoles(x_pos, y_pos)
                    y_pos += 1
                x_pos += 1
                
            def RectangleBoundary(the_output):
                _DrawBorder(the_output, x_number, y_number)
            return RectangleBoundary
                
        # Triplet pythagoricien.
        # 3 - 4 - 5
        # 5 - 12 - 13
        # https://fr.wikipedia.org/wiki/Triplet_pythagoricien
        # Find the closest Pythagorean triple.
        # This creates a right triangle.
        # This is useful to assemble sheets on non-right angles.
        # They could be used to triangularize 3D spline curves.
        def Pythagore(self, x_number, y_number):
            x_iter = x_number
            y_iter = y_number
            # TODO: This is not a very good method to find the next Pythagorean triple.
            while True:
                print("Triangle : Trying x=", x_iter, "y=", y_iter)
                c_square = (x_iter - 1 ) * (x_iter - 1 ) + (y_iter - 1 ) * (y_iter - 1 )
                c_number = int(math.sqrt(c_square))
                if c_number * c_number == c_square:
                    break
                if (x_iter - x_number) / x_number > (y_iter - y_number) / y_number:
                    y_iter += 1
                else:
                    x_iter += 1
            print("Triangle : OK x=", x_iter, "y=", y_iter, "c=", c_number)

            for x_pos_sub in range(x_iter):
                self._AddHoles(x_pos_sub, 0)
            for y_pos_sub in range(y_iter):
                self._AddHoles(0, y_pos_sub)

            def TriangleBoundary(the_output):
                _DrawBorderTriangle(the_output, x_iter, y_iter, c_number)
            return TriangleBoundary


if __name__ == "__main__":
    # python .\meccano.py t_line.dxf Line 10
    # python .\meccano.py t_rect.dxf Rectangle 10 5
    # python .\meccano.py t_rect.dxf Triangle 10 5
    
    function_name = sys.argv[1]
    print("function_name=", function_name)
    
    str_line_arguments = sys.argv[2:]
    filename_end = "_".join(str_line_arguments)
    filename = function_name + "_" + filename_end + ".dxf"
    print("filename=", filename)
    file_output = open(filename, "w");

    int_line_arguments = [int(a) for a in str_line_arguments]

    meccano = MeccanoPart(file_output)
    # Position (0, 0)
    tracer = MeccanoPart.ObjectTracer(meccano, 0, 0)
    function_obj = getattr(tracer, function_name)

    # By convention, all functions return a function which draws the boundary.
    boundary_tracer = function_obj(*int_line_arguments)
    boundary_tracer(file_output)
    
    meccano.DrawDxf()
    meccano.Exit()
    file_output.close()
