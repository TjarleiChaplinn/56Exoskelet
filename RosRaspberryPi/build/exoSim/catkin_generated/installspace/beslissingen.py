#!/usr/bin/env python3

threshholdSensor1 = 200
threshholdSensor2 = 300
freeMode = False

from math import pi
import rospy as ros
from std_msgs.msg import String

pub = ros.Publisher('instructions', String, queue_size=10)

def getTimeFromAngle(degree, speed, armLength):
    distance = (degree / 360) * pi * armLength * 2
    return round(distance / speed, 2)

def freeModeAlgorithm(sensor1, sensor2, limitSensor1, limitSensor2):
    global threshholdSensor1
    global threshholdSensor2
    error, angle, direction = 0, 0, 0
    if limitSensor1 == 1 or limitSensor2 == 1:
        angle = 20
        direction = max(limitSensor2 - limitSensor1, 0)

    elif sensor1 > threshholdSensor1 or sensor2 > threshholdSensor2:
        angle = 10
        if sensor1 > threshholdSensor1:
            direction = 1
        else:
            direction = 0
    time = getTimeFromAngle(angle, 0.3, 0.27)

    instruction = str(time) + '-' + str(direction) + '-' + str(error)
    return instruction

def assistedAlgorithm(sensor1, sensor2, limitSensor1, limitSensor2):
    maxAngle = 30                            #maximale hoek die de arm binnen 1 instructie kan maken
    s1Threshold, s2Threshold = 300, 300     #minimale waarde om de arm te bewegen
    armLength = 0.27                        #lengte van de onderarm
    speed = 0.3                          #snelheid waarmee de arm beweegt(vanaf het eind van de arm)
    #constante om het analoge signaal om te zetten naar een hoek gemeten in graden
    analogToAngle = (1024 - ((s1Threshold + s2Threshold) / 2)) / maxAngle

    #checkt of een van de limieten is bereikt en bepaald de richting waarin de arm terug moet bewegen
    if limitSensor1 or limitSensor2:
        direction = max(limitSensor2 - limitSensor1, 0)
        angle = 20                  #vastgestelde waarde hoe ver de arm terug beweegt
    #checkt of de minimale waarde om de arm te bewegen bereikt is
    elif sensor1 > s1Threshold or sensor2 > s2Threshold:
        #zorgt dat de minimale waarde niet word meegenomen in de berekening
        sensor1 = sensor1 - s1Threshold if sensor1 > s1Threshold else 0
        sensor2 = sensor2 - s2Threshold if sensor2 > s2Threshold else 0
        #berekent de hoek die bepaald hoe ver de arm een richting op beweegt
        angle = (sensor1 - sensor2 if sensor1 >= sensor2 else sensor2 - sensor1) / analogToAngle
        #bepaald welke richting de arm in beweegt
        direction = 1 if sensor1 - sensor2 > 0 else 0
    #als de waarde onder de minimale waarden valt beweegt de arm niet
    else:
        angle = 0
        time = 0
        direction = 0

    #berekent de afstand die de arm moet bewegen aan de hand van een sector van de omtrek van een cirkel
    #waarin de sector de benodigde hoek is
    #bepaalt hoe lang de arm over deze beweging zou doen en hoe lang de motoren dus aan moeten
    time = getTimeFromAngle(angle, speed, armLength)
    #stuurt de instructie met de tijd dat de motoren aan moeten, de richting en dat er geen error was
    return str(time) + '-' + str(direction) + '-0'

def callback(data):
    global freeMode
    if str(data.data).lower() == 'assisted':
        freeMode = False
    else:
        try:
            sensor1, sensor2, limitSensor1, limitSensor2, error = str(data.data).split('-')
            sensor1, sensor2, limitSensor1, limitSensor2, error = int(sensor1), int(sensor2), int(limitSensor1), int(limitSensor2), int(error)
        except ValueError as e:
            print(e)
        if error == 1:
            data = "0-0-1"
            freeMode = True
            pub.publish(data)
            return
        try:
            if freeMode == True:
                data = freeModeAlgorithm(sensor1, sensor2, limitSensor1, limitSensor2)
            else:
                data = assistedAlgorithm(sensor1, sensor2, limitSensor1, limitSensor2)
        except Exception as e:
            print(e)
            freeMode = True
            data = "0-0-1"
        pub.publish(data)

def controller():
    ros.init_node('beslissingen')
    ros.Subscriber('sensordata', String, callback)

    ros.spin()

if __name__ == '__main__':
    controller()