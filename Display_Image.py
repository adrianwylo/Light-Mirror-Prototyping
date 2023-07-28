from curses import panel
import cv2

import board
import neopixel

# Define the parameters of your NeoPixel grid
NUM_PIXELS = 32*64
PIN = board.D18  # Choose the appropriate GPIO pin for your setup

# Initialize the NeoPixel object
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=0.2, auto_write=False)

#--------------------------------------------------------------------------------

def crop_center(image, crop_ratio=(2, 1)):
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Calculate the center coordinates of the image
    center_x = width // 2
    center_y = height // 2

    # Calculate the new width and height after cropping
    new_width = width // crop_ratio[1]
    new_height = width // crop_ratio[0]

    # Calculate the cropping boundaries
    x_start = center_x - new_width // 2
    x_end = center_x + new_width // 2
    y_start = center_y - new_height // 2
    y_end = center_y + new_height // 2

    # Perform cropping
    cropped_image = image[y_start:y_end, x_start:x_end]

    return cropped_image

def pixelate_image(image, pixel_size):
    # Crop the center of the camera view in a 2 by 1 proportion
    cropped_image = crop_center(image, crop_ratio=(2, 1))

    # Get image dimensions
    height, width = cropped_image.shape[:2]

    # Calculate the number of pixels in each dimension
    num_pixels_height = height // pixel_size
    num_pixels_width = width // pixel_size

    # Resize the cropped image to the desired pixelated dimensions
    resized_image = cv2.resize(cropped_image, (num_pixels_width, num_pixels_height), interpolation=cv2.INTER_NEAREST)

    # Upscale the pixelated image to the original dimensions
    pixelated_image = cv2.resize(resized_image, (width, height), interpolation=cv2.INTER_NEAREST)

    return pixelated_image

def show_led_image(frame):
    # Get image dimensions
    if frame is not None:
        height, width = frame.shape[:2]
        print("found height is ", height, "and found width is ", width)
    else:
        print("Error: No image for LED")

    # Calculate the number of pixels per square
    panel_size = 16
    num_pixels_per = height//32
    for y in range(32):
        for x in range(64):
            # Extract RGB values from the pixelated frame
            b, g, r  = frame[int(y * num_pixels_per), int(x * num_pixels_per)]

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
            
            # Set the NeoPixel color
            pixels[pixel_index] = (int(r), int(g), int(b))
        
    # Show the changed pixels on the NeoPixel display
    pixels.show()

#--------------------------------------------------------------------------------


# Define the desired pixel size (adjust as needed)
pixel_size = 5

# Load the image from a file
image_path = "Example_Image.jpg"
frame = cv2.imread(image_path)

if frame is not None:
    print("Image loaded successfully from", image_path)
else:
    print("Error: Unable to load the image from", image_path)
    exit(1)

# Apply pixelation to the frame
pixelated_frame = pixelate_image(frame, pixel_size)

# Show the pixelated frame on the NeoPixel display
show_led_image(pixelated_frame)


if pixelated_frame is not None:
    # Display the image in a window
    cv2.imshow('Pixelated Image', pixelated_frame)

    # Wait until a key is pressed (0 means wait indefinitely)
    cv2.waitKey(1000)

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()
else:
    print("Error: Image not found or unable to load.")
