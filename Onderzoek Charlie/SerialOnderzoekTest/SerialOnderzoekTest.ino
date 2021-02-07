void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() == 0){return;}
  char receivedTime[100] = {};
  int i = 0;
  while (Serial.available() > 0){
    char temp = Serial.read();
    receivedTime[i] = temp;
    i++;
  }
  Serial.write(receivedTime);
}
