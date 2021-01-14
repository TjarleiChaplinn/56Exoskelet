#include <SoftwareSerial.h>
SoftwareSerial mySerial(2,3);
void setup() {
  mySerial.begin(9600);
}

void loop() {
  if(mySerial.available() == 0){return 0;}
  int receivedTime = 0;
  while(mySerial.available() > 0){
    receivedTime = mySerial.read();
  }
  mySerial.write(receivedTime);
}
