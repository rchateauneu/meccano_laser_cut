
from dxflib import *

mecano_step = 12.7
mecano_hole = 2.05

xa = 0
ya = 0
xb = 20 * mecano_step
yb = 10 * mecano_step

def draw_rect(the_output, x1, y1, x2, y2, the_color):
    draw_line_actual(the_output, x1, y1, x1, y2, the_color)
    draw_line_actual(the_output, x1, y2, x2, y2, the_color)
    draw_line_actual(the_output, x2, y2, x2, y1, the_color)
    draw_line_actual(the_output, x2, y1, x1, y1, the_color)

button_diameter = 8
led_diameter = 7

x_cadran = 59
y_cadran = 41

x_offset_cadran = 10
y_offset_cadran = 10

def draw_face_avant():
    the_output = init_output_actual("face_avant.dxf")
    draw_rect(the_output, xa, ya, xb, yb, COLOR_DARK_BLUE)
    draw_rect(the_output, xa + x_offset_cadran, ya + y_offset_cadran, xa + x_offset_cadran + x_cadran, ya + y_offset_cadran + y_cadran, COLOR_BLACK)
    
    y_buttons = ya + y_offset_cadran + y_cadran + 10
    x_space_button = 20

    draw_hole_actual(the_output, x_offset_cadran, y_buttons, button_diameter, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_cadran + x_space_button, y_buttons, button_diameter, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_cadran + 2 * x_space_button, y_buttons, button_diameter, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_cadran + 3 * x_space_button, y_buttons, button_diameter, COLOR_DARK_BLUE)

    y_leds = y_buttons + 15
    x_space_led = 20

    draw_hole_actual(the_output, x_offset_cadran, y_leds, led_diameter, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_cadran + x_space_led, y_leds, led_diameter, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_cadran + 2 * x_space_led, y_leds, led_diameter, COLOR_DARK_BLUE)

    exit_output(the_output)


draw_face_avant()
