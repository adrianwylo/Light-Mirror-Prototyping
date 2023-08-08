import cv2
import board
import neopixel
import threading

# Your existing functions

# ...

# Create threading events
camera_ready = threading.Event()
led_ready = threading.Event()

def camera_thread():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("you messed up")
            break
        frame = cv2.resize(frame, (x, y))
        update_next_colors(frame, col_dictionary, y, x)
        camera_ready.set()  # Signal that the camera thread is ready
        led_ready.wait()    # Wait for the LED thread to be ready
        camera_ready.clear()

def led_thread():
    while True:
        camera_ready.wait()  # Wait for the camera thread to be ready
        shift_led_image(col_dictionary, pos_dictionary, y, x)
        led_ready.set()      # Signal that the LED thread is ready

# Variables
x = 64
y = 32
panel_size = 16
cam_index = 0

# Initialize the NeoPixel object
NUM_PIXELS = x * y
PIN = board.D18  # Choose the appropriate GPIO pin for your setup
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=0.2, auto_write=False)

# Open the video capture
cap = cv2.VideoCapture(cam_index)

# Create Mapping
pos_dictionary = {}
col_dictionary = {}
create_mapping(pos_dictionary, col_dictionary, y, x, panel_size)

# Create and start the camera and LED threads
camera_thread = threading.Thread(target=camera_thread)
led_thread = threading.Thread(target=led_thread)

camera_thread.start()
led_thread.start()

# Wait for both threads to finish
camera_thread.join()
led_thread.join()

# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
# Turn off the LED at the end
pixels.fill((0, 0, 0))
pixels.show()
