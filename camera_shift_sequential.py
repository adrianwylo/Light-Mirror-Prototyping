import cv2
import board
import neopixel
import threading
import time

class LedController:
    def __init__(self, x, y, panel_size, cam_index, steps):
        self.x = x
        self.y = y
        self.total_steps = steps
        self.panel_size = panel_size
        self.cam_index = cam_index
        self.cap_index_odd = True
        self.NUM_PIXELS = x * y
        self.PIN = board.D18
        self.pixels = neopixel.NeoPixel(self.PIN, self.NUM_PIXELS, brightness=0.2, auto_write=False)
        
        self.cap = cv2.VideoCapture(self.cam_index)
        
        self.pos_dictionary = {}
        self.col_ac_dictionary = {}
        self.col_bd_dictionary = {}
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
        #takin da picture (a)

        
                base_pixel = x_panel * (self.panel_size ** 2) * 2 + y_panel * (self.panel_size ** 2)
                y_panel_offset = y % self.panel_size
                x_panel_offset = x % self.panel_size
                if x_panel_offset % 2 == 0:
                    offset_amount = x_panel_offset * self.panel_size + y_panel_offset
                else:
                    offset_amount = (x_panel_offset + 1) * self.panel_size - 1 - y_panel_offset
                pixel_index = base_pixel + offset_amount
                
                self.pos_dictionary[(y, x)] = pixel_index
                self.col_ac_dictionary[(y, x)] = ((0, 0, 0), (0, 0, 0))
                self.col_bd_dictionary[(y, x)] = ((0, 0, 0), (0, 0, 0))
                self.cap_dictionary[(y, x)] = (0, 0, 0)
        
    def camera_thread_function(self):
        #takin da picture (b)
        ret, frame = self.cap.read()
        if not ret:
            print("Error capturing frame (initial)")
        frame = cv2.resize(frame, (self.x, self.y))
        self.capture_colors(frame)
        #do this twice to file up bd_dic with a copied frame
        self.update_next_colors_bd()
        self.update_next_colors_bd()
        #waiting moment lol
        while True:

            #takin da picture (c) and do da rest
            ret, frame = self.cap.read()
            if not ret:
                print("Error capturing frame")
                break
            frame = cv2.resize(frame, (self.x, self.y))
            self.capture_colors(frame)
            if self.cap_index_odd:
                self.update_next_colors_ac()
            else:
                self.update_next_colors_bd()
            self.camera_ready.set()
            self.led_ready.wait()
            self.camera_ready.clear()
            
    def led_thread_function(self):
        while True:
            self.camera_ready.wait()
            if self.cap_index_odd:
                self.cap_index_odd = not self.cap_index_odd
                self.led_ready.set()
                self.shift_trans_led()
                self.shift_led_image_ac()
            else:
                self.cap_index_odd = not self.cap_index_odd
                self.led_ready.set()
                self.shift_trans_led()
                self.shift_led_image_bd()

    def capture_colors(self, frame):
        for y in range(self.y):
            for x in range(self.x):
                b, g, r = frame[int(y), int(x)]
                self.cap_dictionary[(y, x)] = (int(r), int(g), int(b))
                
    def update_next_colors_ac(self):
        for y in range(self.y):
            for x in range(self.x):
                self.col_ac_dictionary[(y, x)] = (self.cap_dictionary[(y, x)], self.col_ac_dictionary[(y, x)][0])
    
    def update_next_colors_bd(self):
        for y in range(self.y):
            for x in range(self.x):
                self.col_bd_dictionary[(y, x)] = (self.cap_dictionary[(y, x)], self.col_bd_dictionary[(y, x)][0])

    def shift_led_image_ac(self):
        print("ac") 
        for stepone in range(self.total_steps + 1):
            interpolated_colors = [
                [
                    self.interpolate_color(
                        self.col_ac_dictionary[(y, x)][0],
                        self.col_ac_dictionary[(y, x)][1],
                        stepone,
                        self.total_steps
                    )
                    for x in range(self.x)
                ]
                for y in range(self.y)
            ]

            for y in range(self.y):
                for x in range(self.x):
                    self.pixels[self.pos_dictionary[(y, x)]] = interpolated_colors[y][x]
            self.pixels.show()
        
    def shift_led_image_bd(self):
        print("bd")
        for step in range(self.total_steps + 1):
            interpolated_colors = [
                [
                    self.interpolate_color(
                        self.col_bd_dictionary[(y, x)][0],
                        self.col_bd_dictionary[(y, x)][1],
                        step,
                        self.total_steps
                    )
                    for x in range(self.x)
                ]
                for y in range(self.y)
            ]

            for y in range(self.y):
                for x in range(self.x):
                    self.pixels[self.pos_dictionary[(y, x)]] = interpolated_colors[y][x]
            self.pixels.show()
    
    def shift_trans_led(self): #note the reversed signs cus of change or something
        print("trans")
        if self.cap_index_odd:
            for step in range(self.total_steps + 1):
                interpolated_colors = [
                    [
                        self.interpolate_color(
                            
                            self.col_bd_dictionary[(y,x)][1],
                            self.pixels[self.pos_dictionary[(y,x)]],
                            step,
                            self.total_steps
                        )
                        for x in range(self.x)
                    ]
                    for y in range(self.y)
                ]
        else:
            for step in range(self.total_steps + 1):
                interpolated_colors = [
                    [
                        self.interpolate_color(
                            
                            self.col_ac_dictionary[(y,x)][1],
                            self.pixels[self.pos_dictionary[(y,x)]],
                            step,
                            self.total_steps
                        )
                        for x in range(self.x)
                    ]
                    for y in range(self.y)
                ]


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
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

# Variables
x = 64
y = 32
panel_size = 16
cam_index = 0
steps = 20

led_controller = LedController(x, y, panel_size, cam_index, steps)
led_controller.run()
