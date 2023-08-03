#include <ArduinoMsgPack.h>
#include <FastLED.h>

#define NUM_PIXELS 64 * 32 // Adjust this according to the size of your LED strip
#define BUFFER_SIZE 256
#define LED_PIN     6

CRGB leds[NUM_PIXELS];
uint8_t buffer[BUFFER_SIZE];

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 bps
  FastLED.addLeds<NEOPIXEL, LED_PIN>(leds, NUM_PIXELS);
  FastLED.show(); // Initialize all LEDs to off(black)
}

void loop() {
  if (Serial.available() > 0) {
    size_t bytesRead = Serial.readBytes(buffer, BUFFER_SIZE);
    // Deserialize the received data
    MsgPack::Reader reader;
    MsgPack::Object object;
    if (reader.parse(buffer, bytesRead, &object)) {
      // Check if the deserialized data is an array
      if (object.isArray()) {
        // Loop through the array and access the individual elements
        for (size_t pos = 0; pos < object.arraySize(); pos++) {
          MsgPack::Object tuple = object[pos];
          // Check if the tuple contains three elements (assuming it's an array of tuples)
          if (tuple.isArray() && tuple.arraySize() == 3) {
            uint8_t r = tuple[0].asInt();
            uint8_t g = tuple[1].asInt();
            uint8_t b = tuple[2].asInt();
            leds[pos] = CRGB(r, g, b);
            FastLED.show();
          }
        }
      }
    }
  }
}
