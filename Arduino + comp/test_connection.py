import serial
import time

# Replace 'COM3' with the appropriate serial port
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

try:
    while True:
        arduino.write(b'ping\n')  # Send a "ping" message to Arduino
        print("Sent: ping")

        response = arduino.readline().decode('utf-8').strip()
        if response == 'pong':
            print("Received:", response)
        else:
            print("Received unexpected response:", response)

        time.sleep(1)  # Wait for 1 second before sending the next ping

except KeyboardInterrupt:
    print("Exiting...")
    arduino.close()


# void setup() {
#     Serial.begin(9600);  // Set the baud rate
# }

# void loop() {
#     if (Serial.available()) {
#         String data = Serial.readStringUntil('\n');
#         data.trim();  // Remove leading/trailing whitespaces

#         if (data == "ping") {
#             Serial.println("pong");
#         }
#     }
# }

