#!/usr/bin/env python3

import rospy as ros
from std_msgs.msg import String
import smbus

#Maakt een bus object aan voor I2C en geeft het een address:
bus = smbus.SMBus(1)
address = 0x09

#Stuurt de instructies naar de arduino via I2C:
def writeString(value):
    intValue = [ord(c) for c in value]
    intValue.append(0)
    for value in intValue:
        bus.write_byte(address, value)

#Haalt de benodigde string uit de data, verstuurt deze naar de arduino en slaat het op in een log:
def sendInstruction(data):
    data = str(data.data)
    writeString(data)
    ros.loginfo(data)

#Leest de instructies van het topic 'instructions', verstuurt deze en regelt de communicatie binnen ROS:
def controller():
    #Initialiseert de node:
    ros.init_node('sendinstructions')
    #Leest de instructies en roept de functie aan om deze naar de arduino te sturen:
    ros.Subscriber("instructions", String, sendInstruction)
    ros.spin()

if __name__ == '__main__':
    controller()