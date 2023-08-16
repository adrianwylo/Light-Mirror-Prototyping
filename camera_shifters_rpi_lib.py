import cv2
import threading
import time
from rpi_ws281x import PixelStrip, Color

class LedController:
    def __init__(self, x, y, panel_size, cam_index):
        self.x = x
        self.y = y
        self.panel_size = panel_size
        self.cam_index = cam_index
        self.NUM_PIXELS = x * y
        self.PIN = 18
        self.LED_FREQ_HZ = 800000
        self.LED_DMA = 10
        self.LED_INVERT = False
        
        # Initialize the WS2815 LED strip
        self.strip = PixelStrip(self.NUM_PIXELS, self.PIN, freq_hz=self.LED_FREQ_HZ, dma=self.LED_DMA, invert=self.LED_INVERT, brightness=255)
        self.strip.begin()
        
        self.cap = cv2.VideoCapture(self.cam_index)
        
        self.pos_dictionary = {}
        self.col_dictionary = {}
        self.cap_dictionary = {}
        
        self.create_mapping()
        
        self.camera_ready = threading.Event()
        self.led_ready = threading.Event()
        
        self.camera_thread = threading.Thread(target=self.camera_thread_function)
        self.led_thread = threading.Thread(target=self.led_thread_function)
        
        self.camera_thread.start()
        self.led_thread.start()
        
    def create_mapping(self):
        for y in range(self.y):
            for x in range(self.x):
                y_panel = int(y // self.panel_size)
                x_panel = int(x // self.panel_size)
                base_pixel = x_panel * (self.panel_size ** 2) * 2 + y_panel * (self.panel_size ** 2)
                y_panel_offset = y % self.panel_size
                x_panel_offset = x % self.panel_size
                if x_panel_offset % 2 == 0:
                    offset_amount = x_panel_offset * self.panel_size + y_panel_offset
                else:
                    offset_amount = (x_panel_offset + 1) * self.panel_size - 1 - y_panel_offset
                pixel_index = base_pixel + offset_amount
                
                self.pos_dictionary[(y, x)] = pixel_index
                self.col_dictionary[(y, x)] = ((0, 0, 0), (0, 0, 0))
                self.cap_dictionary[(y, x)] = (0, 0, 0)
        
    def camera_thread_function(self):
        while True:
            #add wait time
            time.sleep(120)
            ret, frame = self.cap.read()
            if not ret:
                print("Error capturing frame")
                break
            frame = cv2.resize(frame, (self.x, self.y))
            self.capture_colors(frame)
            self.camera_ready.set()
            self.led_ready.wait()
            self.camera_ready.clear()
            
    def led_thread_function(self):
        while True:
            self.camera_ready.wait()
            self.update_next_colors()
            self.led_ready.set()
            self.shift_led_image()
            

    def capture_colors(self, frame):
        for y in range(self.y):
            for x in range(self.x):
                b, g, r = frame[int(y), int(x)]
                self.cap_dictionary[(y, x)] = (int(r), int(g), int(b))
                
    def update_next_colors(self):
        for y in range(self.y):
            for x in range(self.x):
                self.col_dictionary[(y, x)] = (self.cap_dictionary[(y, x)], self.col_dictionary[(y, x)][0])
    
    def shift_led_image(self):
        total_steps = 5  # Changeable
        for step in range(total_steps + 1):
            for y in range(self.y):
                for x in range(self.x):
                    pixel_index = self.pos_dictionary[(y, x)]
                    color = self.interpolate_color(self.col_dictionary[(y, x)][0], self.col_dictionary[(y, x)][1], step, total_steps)
                    self.strip.setPixelColor(pixel_index, Color(*color))
            self.strip.show()
    
    def interpolate_color(self, color2, color1, step, total_steps):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        new_r = int(r1 + (step * (r2 - r1) / total_steps))
        new_g = int(g1 + (step * (g2 - g1) / total_steps))
        new_b = int(b1 + (step * (b2 - b1) / total_steps))
        return new_r, new_g, new_b

    def run(self):
        self.camera_thread.join()
        self.led_thread.join()
        self.cap.release()
        cv2.destroyAllWindows()
        self.strip.fill(0)  # Turn off LEDs
        self.strip.show()

# Variables
x = 64
y = 32
panel_size = 16
cam_index = 0

led_controller = LedController(x, y, panel_size, cam_index)
led_controller.run()
