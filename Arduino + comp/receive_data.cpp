// #include <Arduino.h>
// #include <MsgPack.h>

// const int bufferSize = 128;
// uint8_t buffer[bufferSize];

// void setup() {
//     Serial.begin(9600);
// }

// void loop() {
//     if (Serial.available() > 0) {
//         size_t bytesRead = Serial.readBytesUntil('\0', (char*)buffer, bufferSize);
        
//         MessagePack::Unpacker unpacker;
//         unpacker.feed(buffer, bytesRead);

//         MessagePack::ObjectHandle objectHandle;
//         while (unpacker.next(objectHandle)) {
//             if (objectHandle.is<ArrayHandle>()) {
//                 auto array = objectHandle.as<ArrayHandle>();
//                 for (size_t i = 0; i < array.size(); ++i) {
//                     if (array[i].is<int>()) {
//                         int value = array[i].as<int>();
//                         Serial.print(value);
//                         Serial.print("\t");
//                     }
//                 }
//                 Serial.println();
//             }
//         }
//     }
// }



#include <Arduino.h>

const int numRows = 256;
const int numCols = 3;

void setup() {
    Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    for (int row = 0; row < numRows; ++row) {
        for (int col = 0; col < numCols; ++col) {
          int value = Serial.parseInt();
          Serial.print(value);
          Serial.print("\t");
        }
        Serial.println("pong");
    }
  }
}

