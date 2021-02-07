#!/usr/bin/env python

import rospy as ros
from std_msgs.msg import String
import smbus

#Maakt een bus object aan voor I2C en geeft het een address:
bus = smbus.SMBus(1)
address = 0x09

#Plaatst de ontvangen set van instructies in een enkele string:
def readString(value):
    #Plaatst de ontvangen bytes in een list:
    byte_list = []
    for _ in range(0,value):
        try:
            byte_list.append(bus.read_byte(address))
        except IOError:
            byte_list.append(0)

    #Als er geen instructies ontvangen zijn en de lijst dus leeg is word een null-terminator gereturned:
    if byte_list[0] == 0:
        return "\0"

    #Plaatst de losse bytes in een string genaamd result die de volledige set van instructies voorstelt:
    result = ""
    for byte in byte_list:
        if byte != 0:
            result = result + chr(byte)
    #Returned de volledige set van instructies:
    return result

def controller():
    #Maakt een publisher object met een queue van maximaal 10 messages:
    pub = ros.Publisher('sensordata', String, queue_size=10)
    #Initialiseert de node:
    ros.init_node('receivedata')
    rate = ros.Rate(1)

    #Zorgt voor een constante stroom van instructies naar het topic sensordata:
    while not ros.is_shutdown():
        temp = readString(16)
        if temp[0] != '\0':
            pub.publish(temp)
            ros.loginfo(temp)
        rate.sleep()


if __name__ == '__main__':
    controller()