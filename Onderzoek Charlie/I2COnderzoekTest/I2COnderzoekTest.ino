#include <Wire.h>
char receivedTime[100] = {};
void setup() {
  Wire.begin(9);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(sendEvent);
}

void loop() {
}

void receiveEvent() {
  int i = 0;
  while(Wire.available() > 0){
    int temp = Wire.read();
    receivedTime[i] = char(temp);
    i++;
  }
}

void sendEvent() {
  Wire.write(receivedTime);
}
