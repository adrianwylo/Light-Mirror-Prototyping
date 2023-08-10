from rpi_ws281x import PixelStrip, Color
import time

# LED strip configuration:
LED_COUNT = 60
LED_PIN = 18  # Use a valid GPIO pin number
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

try:
    while True:
        # Cycle through colors
        for i in range(256):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(i, 255 - i, 0))
            strip.show()
            time.sleep(0.02)
except KeyboardInterrupt:
    # Turn off the LEDs and clean up
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
