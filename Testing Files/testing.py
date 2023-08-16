import board
import neopixel

# Define the parameters of your NeoPixel grid
NUM_PIXELS = 32*64
PIN = board.D18  # Choose the appropriate GPIO pin for your setup

# Initialize the NeoPixel object
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=0.2, auto_write=False)
panel_size = 16
for y in range(32):
        for x in range(64):
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
            pixels[pixel_index] = (255, 200, 60)
# Show the changed pixels on the NeoPixel display
pixels.show()