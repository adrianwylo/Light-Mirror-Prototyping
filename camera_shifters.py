import cv2
import board
import neopixel
import numpy as np

def shift_led_image(c_dic, p_dic, b, a):
    for y in range(b):
            for x in range(a):
                total_steps = 100 #changeable
                interpolate_color(dictionary)
                for step in range(total_steps + 1):
                    pixels[p_dic[(y,x)]] = interpolate_color(c_dic[(y,x)][0], c_dic[(y,x)][1], step, total_steps)
                    pixels.show()

# Function to interpolate between two colors
def interpolate_color(color1, color2, step, total_steps):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    new_r = int(r1 + (step * (r2 - r1) / total_steps))
    new_g = int(g1 + (step * (g2 - g1) / total_steps))
    new_b = int(b1 + (step * (b2 - b1) / total_steps))
    return (new_r, new_g, new_b)

def update_next_colors(frame, c_dic, b, a):
    for y in range(b):
            for x in range(a):
                b, g, r = frame[int(y), int(x)]
                c_dic[(y,x)] = ((c_dic[(y,x)][0][0], c_dic[(y,x)][0][1], c_dic[(y,x)][0][2]),(int(r), int(g), int(b)))
            

def create_mapping(my_dictionary, my_c_dictionary, b, a, panel_size):
    # make dictionary mapping
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
            # Mapping
            pixel_index = base_pixel + offset_amount
            my_dictionary[(y,x)] = pixel_index
            my_c_dictionary[(y,x)] = ((0, 0, 0), (0, 0, 0))

#Variables
x = 64
y = 32
panel_size = 16
cam_index = 0

# Initialize the NeoPixel object
NUM_PIXELS = x * y
PIN = board.D18  # Choose the appropriate GPIO pin for your setup
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=0.2, auto_write=False)

# Open the video capture
cap = cv2.VideoCapture(0) 

#Create Mapping
pos_dictionary = {}
col_dictionary = {}
create_mapping(my_dictionary, col_dictionary y, x, panel_size)

#Camera Loop
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print("you messed up")
        break
    frame = cv2.resize(frame, (x, y))

    update_next_colors(frame, col_dictionary, y, x)

    shift_led_image(col_dictionary, pos_dictionary, y, x)

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
# Turn off the LED at the end
pixels.fill((0, 0, 0))
pixels.show()