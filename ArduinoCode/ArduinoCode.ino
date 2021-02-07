#include <Wire.h>
#include <ros.h>
#include <std_msgs/String.h>

char inputChr[16] = "";
bool haveWord = false;

void callback(const std_msgs::String& msg){
  String temp = msg.data;
  for(int i = 0; i < temp.length(); i++){
    inputChr[i] = temp[i];
  }
  haveWord = true;
}

std_msgs::String str_msg;
ros::NodeHandle nh;
ros::Subscriber<std_msgs::String> sensordata("sensordata", &callback);
ros::Publisher instructions("instructions", &str_msg);

void setup() {
  Wire.begin(9);
  Serial.begin(115200);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(sendEvent);
  nh.initNode();
  nh.advertise(instructions);
  nh.subscribe(sensordata);
}

void loop() {
  nh.spinOnce();
  delay(1);
}

char instructionChr[16];
int index = 0;

void sendData(){
  str_msg.data = instructionChr;
  instructions.publish(&str_msg);
  index = 0;
}

void receiveEvent() {
  char temp = Wire.read();
  instructionChr[index] = temp;
  if(instructionChr[index] == byte(0)){
    sendData();
  }
  index++; 
}

int sendChar = 0;

void sendEvent() {
  if(!haveWord){
    for(int i = 0; i<16;i++){
      inputChr[i] = byte(0);
    }
    Wire.write(byte(0));
  }
  else{
    Wire.write(inputChr[sendChar]);
    sendChar++;
    if(sendChar >= 15){
      haveWord = false;
      sendChar = 0;
    }
  }
}
