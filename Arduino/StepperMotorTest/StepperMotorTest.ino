#include <TimedAction.h>

// defines pins numbers
const int stepPin = 3; 
const int dirPin = 4; 
const int stepPin2 = 5;
const int dirPin2 = 6;

boolean stopBool = false;

void changePins();

TimedAction motorThread = TimedAction(1, changePins);

void setup() {
  Serial.begin(9600);
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  digitalWrite(dirPin,HIGH);
  digitalWrite(dirPin2,HIGH);
}

char temp = '0';

void loop() {
  motorThread.check();
  while(Serial.available() == 0){return;}
  int number = Serial.parseInt();
  if(number == 1){
    digitalWrite(dirPin,HIGH);
  }
  else if(number == 2){
    digitalWrite(dirPin,LOW);
  }
  else if(number == 3){
    digitalWrite(dirPin2,HIGH);
  }
  else if(number == 4){
    digitalWrite(dirPin2,LOW);
  }
  /*while(Serial.available() == 0) {motorThread.check(); stopBool = false; return;}
  if (Serial.available() > 0){
    temp = Serial.read();
  }
  if(temp == 'r'){
    stopBool = false;
    digitalWrite(dirPin,HIGH);
  }
  else if(temp == 'l'){
    stopBool = false;
    digitalWrite(dirPin,LOW);
  }
  else if(temp == 'u'){
    stopBool = false;
    digitalWrite(dirPin2,HIGH);
  }
  else if(temp == 'd'){
    stopBool = false;
    digitalWrite(dirPin2,LOW);
  }
  else {
    stopBool = true;
  }*/
}

boolean onState = false;

void changePins(){
  if(!stopBool){
    if(onState){
      digitalWrite(stepPin,LOW);
      digitalWrite(stepPin2,LOW);
    }
    else{
      digitalWrite(stepPin,HIGH);
      digitalWrite(stepPin2,HIGH);
    }
    onState = !onState;
  }
}
