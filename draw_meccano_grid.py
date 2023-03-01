# This draws a Meccano grid which can be used as a pattern for drilling.

from PIL import Image
from PIL import ImageDraw

pixel_per_mm = 10

# Meccano system dates back to 1901 and is designed to Imperial sizes ie 1/2 inch hole spacings
# Plain holes in all Meccano parts are all 4.1mm in diameter, and are spaced at 1/2" (12.7mm),
# with some modern parts having twice as many holes to give a 1/4" (6.3mm) spacing.
# Meccano axles are a running fit in the holes, and are 4.06mm in diameter.
# This is actually an old Imperial SWG (Standard Wire Gauge) size 8.
meccano_step_mm = 12.7
meccano_step_pixels = meccano_step_mm * pixel_per_mm

meccano_hole_radius_mm = 2.05
meccano_hole_radius_pixels = meccano_hole_radius_mm * pixel_per_mm
page_width = 210
page_height = 297


## 254 dots per inches, one dot is 1/0 mm.
dpi = 254

image_pixels_width = page_width * pixel_per_mm
image_pixels_height = page_height * pixel_per_mm

pattern_image = Image.new('RGBA', (image_pixels_width, image_pixels_height), (255, 255, 255))
pattern_image.info['dpi'] = dpi

image_draw = ImageDraw.Draw(pattern_image)

# No attempt to optimize things because this is not worth here.
index_width = 0.5
while True:
    hole_x = index_width * meccano_step_pixels
    if hole_x > image_pixels_width:
        break
    index_height = 0.5
    while True:
        hole_y = index_height * meccano_step_pixels
        if hole_y > image_pixels_height:
            break
        hole_left = hole_x - meccano_hole_radius_pixels
        hole_right = hole_x + meccano_hole_radius_pixels
        hole_upper = hole_y - meccano_hole_radius_pixels
        hole_lower = hole_y + meccano_hole_radius_pixels
        # image_draw.ellipse((hole_left, hole_upper, hole_right, hole_lower), fill = 'blue', outline ='blue')
        image_draw.ellipse((hole_left, hole_upper, hole_right, hole_lower), outline ='blue')
        image_draw.line((hole_x, hole_y - meccano_hole_radius_pixels, hole_x, hole_y + meccano_hole_radius_pixels), 'red')
        image_draw.line((hole_x - meccano_hole_radius_pixels, hole_y, hole_x + meccano_hole_radius_pixels, hole_y), 'red')
        # image_draw.point((hole_x, hole_y), 'red')
        index_height += 1
    index_width += 1

pattern_image.save('meccano_pattern.png')

