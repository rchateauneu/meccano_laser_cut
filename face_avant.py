
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

button_radius = 3.5
led_radius = 2.5

x_cadran = 59
y_cadran = 41

x_offset_cadran = 10
y_offset_cadran = 10

def draw_face_avant():
    the_output = init_output_actual("face_avant.dxf")
    draw_rect(the_output, xa, ya, xb, yb, COLOR_DARK_BLUE)
    draw_rect(the_output, xa + x_offset_cadran, ya + y_offset_cadran, xa + x_offset_cadran + x_cadran, ya + y_offset_cadran + y_cadran, COLOR_BLACK)
    
    y_buttons = ya + y_offset_cadran + y_cadran + 10
    x_space_button = x_cadran / 4

    x_offset_button = x_offset_cadran
    draw_hole_actual(the_output, x_offset_button + 0.5 * x_space_button, y_buttons, button_radius, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_button + 1.5 * x_space_button, y_buttons, button_radius, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_button + 2.5 * x_space_button, y_buttons, button_radius, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_button + 3.5 * x_space_button, y_buttons, button_radius, COLOR_DARK_BLUE)

    # y_leds = y_buttons + 15
    y_space_led = y_cadran / 3

    #draw_hole_actual(the_output, x_offset_cadran, y_leds, led_radius, COLOR_DARK_BLUE)
    #draw_hole_actual(the_output, x_offset_cadran + x_space_led, y_leds, led_radius, COLOR_DARK_BLUE)
    #draw_hole_actual(the_output, x_offset_cadran + 2 * x_space_led, y_leds, led_radius, COLOR_DARK_BLUE)
    x_offset_leds = xa + x_offset_cadran + x_cadran + 10
    y_leds = y_offset_cadran

    draw_hole_actual(the_output, x_offset_leds, y_leds + 0.5 * y_space_led, led_radius, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_leds, y_leds + 1.5 * y_space_led, led_radius, COLOR_DARK_BLUE)
    draw_hole_actual(the_output, x_offset_leds, y_leds + 2.5 * y_space_led, led_radius, COLOR_DARK_BLUE)

    exit_output(the_output)


draw_face_avant()
