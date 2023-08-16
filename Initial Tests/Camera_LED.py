import cv2
import board
from apa102_pi.driver import apa102


def show_led_image(frame, dictionary, b, a):
    for y in range(b):
            for x in range(a):
                b, g, r = frame[int(y), int(x)]
                pixels.set_pixel_rgb(dictionary[(y,x)], r<<16 + g << 8 + b)
    pixels.show()
    pixels.cleanup()
    
def create_mapping(my_dictionary, b, a, panel_size):
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

#Variables
x = 32
y = 16
panel_size = 16
cam_index = 0

# Initialize the NeoPixel object
NUM_PIXELS = x * y
PIN = board.D18  # Choose the appropriate GPIO pin for your setup
pixels = apa102.APA102(num_led=NUM_PIXELS, order='rgb')

# Open the video capture
cap = cv2.VideoCapture(0) 

#Create Mapping
my_dictionary = {}
create_mapping(my_dictionary, y, x, panel_size)

#Camera Loop
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print("you messed up")
        break
    frame = cv2.resize(frame, (x, y))

    # Show the pixelated frame on the NeoPixel display
    show_led_image(frame, my_dictionary, y, x)
    print("check")
    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
