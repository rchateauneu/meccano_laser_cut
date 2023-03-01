
# https://gohtx.com/acadcolors.php
COLOR_BLACK = 0
COLOR_LIGHT_BLUE = 4
COLOR_DARK_BLUE = 5

def init_output_actual(path_name):
    the_output = open(path_name, "w")
    the_output.write("""\
0
SECTION
2
ENTITIES
""")
    return the_output


def exit_output(the_output):
    the_output.write("""\
0
ENDSEC
0
EOF
""")
    the_output.close()


def draw_line_actual(the_output, x_start, y_start, x_end, y_end, line_color):
    the_output.write("""\
0
LINE
8
Undeflected
10
%lf
20
%lf
11
%lf
21
%lf
62
%d
""" % (x_start, y_start, x_end, y_end, line_color))


def draw_hole_actual(the_output, x_pos, y_pos, hole_diameter, hole_color):
    the_output.write("""\
0
CIRCLE
8
Undeflected
10
%lf
20
%lf
30
0.0
40
%lf
62
%d
""" % (x_pos, y_pos, hole_diameter, hole_color))
