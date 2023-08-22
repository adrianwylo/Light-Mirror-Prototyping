import cv2
import board
from apa102_pi.driver import apa102

def shift_led_image(c_dic, p_dic, b, a, pixels):
    total_steps = 20  # changeable
    for step in range(total_steps + 1):
        for y in range(b):
            for x in range(a):
                pixels.set_pixel_rgb(p_dic[(y, x)], interpolate_color(c_dic[(y, x)][0], c_dic[(y, x)][1], step, total_steps))
        pixels.show()

def interpolate_color(color2, color1, step, total_steps):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    new_r = int(r1 + (step * (r2 - r1) / total_steps))
    new_g = int(g1 + (step * (g2 - g1) / total_steps))
    new_b = int(b1 + (step * (b2 - b1) / total_steps))
    return (new_r<<16) + (new_g << 8) + new_b

def tint_grayscale(gray_value, tint_color):
    # Apply the tint color to the grayscale value
    r_tint, g_tint, b_tint = tint_color
    r_tinted = min(255, max(0, gray_value + r_tint))
    g_tinted = min(255, max(0, gray_value + g_tint))
    b_tinted = min(255, max(0, gray_value + b_tint))
    return r_tinted, g_tinted, b_tinted

def update_next_colors(frame, c_dic, b, a, tint_color):
    for y in range(b):
        for x in range(a):
            r, g, b = frame[int(y), int(x)]
            # Convert to grayscale using luminance formula: 0.2989 * R + 0.5870 * G + 0.1140 * B
            gb = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            c_dic[(y, x)] = (tint_grayscale(gb, tint_color), 
                             (c_dic[(y, x)][0][0], c_dic[(y, x)][0][1], c_dic[(y, x)][0][2]))
            
def create_mapping(my_dictionary, my_c_dictionary, b, a, panel_size):
    for y in range(b):
        for x in range(a):
            y_panel = int(y // panel_size)
            x_panel = int(x // panel_size)
            base_pixel = x_panel * (panel_size ** 2) * 2 + y_panel * (panel_size ** 2)
            y_panel_offset = y % panel_size
            x_panel_offset = x % panel_size
            if x_panel_offset % 2 == 0:
                offset_amount = x_panel_offset * panel_size + y_panel_offset
            else:
                offset_amount = (x_panel_offset + 1) * panel_size - 1 - y_panel_offset
            pixel_index = base_pixel + offset_amount
            my_dictionary[(y, x)] = pixel_index
            my_c_dictionary[(y, x)] = ((0, 0, 0), (0, 0, 0))

x = 32
y = 16
panel_size = 16
NUM_PIXELS = x * y

# Define the cropping region's top-left corner and dimensions
crop_x = 100
crop_y = 100
crop_width = 200
crop_height = 200

cam_index = 0 #cam index

tint_color = (255, 0, 0) #Red

pixels = apa102.APA102(num_led=NUM_PIXELS, order='rgb')

cap = cv2.VideoCapture(cam_index)

pos_dictionary = {}
col_dictionary = {}

#map coordinates to pixel #
create_mapping(pos_dictionary, col_dictionary, y, x, panel_size)

while True:
    #capture pic
    ret, frame = cap.read()
    if not ret:
        print("Capture error")
        break
    
    # Crop the frame to the defined region
    cropped_frame = frame[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]

    # Resize cropped frame to match panel dimensions
    frame = cv2.resize(cropped_frame, (x, y))

    #process frame
    update_next_colors(frame, col_dictionary, y, x, tint_color)

    #display
    shift_led_image(col_dictionary, pos_dictionary, y, x)
    

cap.release()
cv2.destroyAllWindows()
pixels.clear_strip()