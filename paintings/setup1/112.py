import cv2
import board
import neopixel

def shift_led_image(c_dic, p_dic, b, a, total_steps):
    for step in range(total_steps + 1):
        for y in range(b):
            for x in range(a):
                color = interpolate_color(c_dic[(y, x)][0], c_dic[(y, x)][1], step, total_steps)
                pixels[p_dic[(y, x)]] = color
    pixels.show()

# helper Function to interpolate between two colors
def interpolate_color(color2, color1, step, total_steps):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    new_r = int(r1 + (step * (r2 - r1) / total_steps))
    new_g = int(g1 + (step * (g2 - g1) / total_steps))
    new_b = int(b1 + (step * (b2 - b1) / total_steps))
    return new_r, new_g, new_b

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
            
            

def create_mapping(mapping, color_bank, b, a, panel_size, display_mode, ):
    y_indexes = [i for i in range(b)]
    x_indexes = [j for j in range(a)]
    #flips initial mapping
    if display_mode == "normal":
        x_indexes.sort(reverse=True)

    #base mapping
    if tilted == "right":
        
    
    elif tilted == "left":

    elif tilted == "up":
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
                mapping[(y, b - x - 1)] = pixel_index
                color_bank[(y, x)] = ((0, 0, 0), (0, 0, 0))

    else:
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
                mapping[(y, b - x - 1)] = pixel_index
                color_bank[(y, x)] = ((0, 0, 0), (0, 0, 0))
                    

x = 16 #X dimension of panel
y = 32 #Y dimension of panel
panel_size = 16 #dimension of panel
NUM_PIXELS = x * y

display_mode = "normal" #Options: "normal", "mirrored"
tilted = "left" #Options: "normal", "left", "right", "up"

cam_index = 0 #cam index

tint_color = (0, 255, 0) #Red

PIN = board.D18 #pin 
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=0.2, auto_write=False)

total_steps = 5  # total step amount

cap = cv2.VideoCapture(cam_index)

pos_dictionary = {}
col_dictionary = {}

#map coordinates to pixel 

create_mapping(pos_dictionary, col_dictionary, y, x, panel_size, display_mode, tilted)

while True:
    #capture pic
    ret, frame = cap.read()
    if not ret:
        print("Capture error")
        break

    # Resize cropped frame to match panel dimensions (separate from matrix dimensions)
    if tilted == "left" or tilted == "right":
        frame = cv2.resize(frame, (y,x))
    else:
        frame = cv2.resize(frame, (x, y))

    #process frame
    update_next_colors(frame, col_dictionary, y, x, tint_color)

    #display
    shift_led_image(col_dictionary, pos_dictionary, y, x, total_steps)
    

cap.release()
cv2.destroyAllWindows()
pixels.fill((0, 0, 0))
pixels.show()
