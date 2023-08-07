#include <MsgPack.h>
#include <FastLED.h>

#define NUM_PIXELS 64 * 32
#define BUFFER_SIZE 256
#define LED_PIN     6

CRGB leds[NUM_PIXELS];
uint8_t buffer[BUFFER_SIZE];

void setup() {
  // Initialize serial communication at 9600 bps
  Serial.begin(9600);
  
  FastLED.addLeds<NEOPIXEL, LED_PIN>(leds, NUM_PIXELS);
  FastLED.show(); // Initialize all LEDs to off(black)
}

void loop() {
  // Check if there is a complete set of data available on the serial port
  if (Serial.available() >= BUFFER_SIZE) {
    // Read the data into the buffer
    Serial.readBytes(buffer, BUFFER_SIZE);

    // Parse the serialized data and update the leds array
    for (int i = 0; i < NUM_PIXELS; i++) {
      int offset = i * 3; // Each LED has 3 bytes (R, G, B)
      uint8_t r = buffer[offset];
      uint8_t g = buffer[offset + 1];
      uint8_t b = buffer[offset + 2];
      leds[i] = CRGB(r, g, b);
    }

    // Show the updated LEDs
    FastLED.show();
  }
}
