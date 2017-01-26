/*
  This sketch reads the lidar distance data and writes the value as cm and
  inches to the serial port. It is written in a form that can be evaled in
  python as a tuple, e..g., (155, 61.02)
 */

unsigned long lastVal = 0;
unsigned long pulseWidth;

void setup() {
  Serial.begin(115200); // Start serial communications

  pinMode(2, OUTPUT); // Set pin 2 as trigger pin
  digitalWrite(2, LOW); // Set trigger LOW for continuous read

  pinMode(3, INPUT); // Set pin 3 as monitor pin
}

void loop() {
  pulseWidth = pulseIn(3, HIGH); // Count how long the pulse is high in microseconds

  if(pulseWidth != 0) {
    pulseWidth = pulseWidth / 10; // 10usec = 1 cm of distance
    if (pulseWidth != 0 && lastVal != pulseWidth) {
      Serial.println("(" + String(pulseWidth) + ", " + String(pulseWidth * 0.393701) + ")");
      delay(200);
   }
  }

  lastVal = pulseWidth;
}
