#!/usr/bin/env python

import rospy as ros
from std_msgs.msg import String
from math import pi

class customAlgorithm:
    def __init__(self, thresholdSensor1, thresholdSensor2, maxAngle, armLength, speed):
        #Stelt de thresholdwaardes in:
        self.thresholdSensor1 = thresholdSensor1
        self.thresholdSensor2 = thresholdSensor2

        #Stelt de fysieke parameters van de arm in:
        self.maxAngle = maxAngle        #(in 1 beweging)
        self.armLength = armLength
        self.speed = speed

        #Stelt de huidige staat van de arm in:
        self.firstRun = True
        self.freeMode = False
        self.previousSensorData = [thresholdSensor1,thresholdSensor2]
        self.simulationMode = True
    
    #Berekend de tijd dat de motoren aan moeten:
    def getTimeFromAngle(self, degree, speed, armLength):
        #Als de arm niet bewogen hoeft te worden kan de berekening overgeslagen worden:
        if degree == 0:
            return 0
        #De afstand word bepaald aan de hand van een sector van de omtrek van de draaicirkel van de arm
        #(de sector is de hoek die de arm moet bewegen)
        distance = (degree / 360) * pi * self.armLength * 2
        return round(distance / self.speed, 2)
    
    #Algoritme voor Assisted Mode:
    def assistedAlgorithm(self, sensor1, sensor2, limitSensor1, limitSensor2):
        #Onder de threshold kan de huidige positie behouden worden:
        angle = 0
        time = 0
        direction = 0

        #Schaalvariabele voor het berekenen van de hoek:
        analogToAngle = (1024 - ((self.thresholdSensor1 + self.thresholdSensor2) / 2)) / self.maxAngle

        print(sensor1, sensor2, limitSensor1, limitSensor2)

        #Arm corrigeert als er over de limieten heen bewogen wordt:
        if limitSensor1 or limitSensor2:
            direction = max(limitSensor1 - limitSensor2, 0)
            angle = 20
        
        #Als de sensorwaarde boven de threshold ligt word de benodigde hoek berekent:
        elif sensor1 > self.thresholdSensor1 or sensor2 > self.thresholdSensor2:
            #Thresholdwaarde wordt niet meegenomen in de berekening
            sensor1 = sensor1 - self.thresholdSensor1 if sensor1 > self.thresholdSensor1 else 0
            sensor2 = sensor2 - self.thresholdSensor2 if sensor2 > self.thresholdSensor2 else 0
            
            #Draairichting van de arm:
            direction = 1 if sensor1 > sensor2 else 0
            #Berekening van de benodigde hoek:
            angle = (sensor1 - sensor2 if direction == 1 else sensor2 - sensor1) / analogToAngle

        #De simulatie heeft alleen de hoek nodig dus deze kan gereturned worden:
        if self.simulationMode:
            angle = round(angle, 2)
            instructions = str(angle) + '-' + str(direction) + '-0'
            print(instructions)
            return instructions

        #Tijd dat de motoren aan moeten:
        time = self.getTimeFromAngle(angle, self.speed, self.armLength)
        
        #Plaatst het resultaat in een string en returned deze:
        instructions = str(time) + '-' + str(direction) + '-0'
        return instructions

    #Algoritme voor Free Mode:
    def freeModeAlgorithm(self, sensor1, sensor2, limitSensor1, limitSensor2):
        #Als er niet bewogen moet worden staat de hoek en richting van de arm op 0:
        angle = 0
        direction = 0

        #Arm corrigeert als er over de limieten heen bewogen wordt:
        if limitSensor1 or limitSensor2:
            angle = 20
            direction = max(limitSensor1 - limitSensor2, 0)

        #Als de sensorwaarde boven de threshold ligt word de benodigde hoek berekent:
        elif sensor1 > self.thresholdSensor1 or sensor2 > self.thresholdSensor2:
            #In Free Mode beweegt de arm met een vastgestelde hoek:
            angle = 10
            #Draairichting van de arm:
            direction = 1 if sensor1 - sensor2 > 0 else 0

        #De simulatie heeft alleen de hoek nodig dus deze kan gereturned worden:
        if self.simulationMode:
            instructions = str(angle) + '-' + str(direction) + '-0'
            return instructions

        #Tijd dat de motoren aan moeten:
        time = self.getTimeFromAngle(angle, 0.3, 0.27)

        #Na de corrigerende beweging gaat de arm uit Free Mode:
        self.freeMode = False

        #Plaatst het resultaat in een string en returned deze:
        instruction = str(time) + '-' + str(direction) + '-0'
        return instruction

    #Corrigeert de eventuele uitschieters in de sensordata:
    def checkForOutliers(self, sensor1, sensor2):
        try:
            #De eerste sensordata is vaak incorrect, deze worden dus genegeerd:
            if self.firstRun:
                self.firstRun = False

            #Bij de opvolgende waarden worden de uitschieters wel weg gefilterd:
            else:
                #Bij een verdubbeling van de sensorwaarde word deze vervangen door de vorige waarden:
                #(Hiermee worden uitschieters weggewerkt maar zal er geen overbodige kracht gezet worden gezet door de gebruiker als dit algoritme een fout maakt)
                if sensor1 > self.previousSensorData[0]  * 4 or sensor2 > self.previousSensorData[1] * 4:
                    sensor1 = self.previousSensorData[0]
                    sensor2 = self.previousSensorData[1]
                #De sensordata word alleen onthouden als deze boven de threshold ligt:
                if sensor1 > self.thresholdSensor1:
                    self.previousSensorData[0] = sensor1
                if sensor2 > self.thresholdSensor2:
                    self.previousSensorData[1] = sensor2
        
        except Exception as e:
            print(e)
            sensor1 = 0
            sensor2 = 0
        
        return sensor1, sensor2

#Maakt een publisher object met een queue van maximaal 10 messages:
pub = ros.Publisher('instructions', String, queue_size=10)

#Maakt een object voor de uitvoering van algoritmes:
calc = customAlgorithm(200, 200, 30, 0.27, 0.3)

def callback(data):
    #Afhandeling van de instructie om Assisted Mode in te schakelen:
    if str(data.data).lower() == 'assisted':
        calc.freeMode = False
    else:
        #Instructies uit de ontvangen string halen en omzetten naar integers voor gebruik:
        try:
            sensor1, sensor2, limitSensor1, limitSensor2, error = str(data.data).split('-')
            limitSensor1, limitSensor2, error =int(limitSensor1), int(limitSensor2), int(error)
        except ValueError as e:
            data = "0-0-0"
            ros.loginfo(data)
            pub.publish(data)
            return
        print("In callback", sensor1, sensor2, limitSensor1, limitSensor2)
        #Eventuele uitschieters in sensordata corrigeren:
        try:
            sensor1, sensor2 = calc.checkForOutliers( int(sensor1), int(sensor2))
        except ValueError as e:
            data = "0-0-0"
            ros.loginfo(data)
            pub.publish(data)
            return
        #Error handling in het geval dat de hardware een fout aangeeft:
        if error == 1:
            data = "0-0-1"
            calc.freeMode = True
            pub.publish(data)
            return
        try:
            #Als beide limietsensoren aan staan geeft dit een error:
            if limitSensor1 and limitSensor2:
                raise Exception('Error: Beide limietsensoren tegelijk geactiveerd!')
            #Als de arm in Free Mode staat word het algoritme daarvoor gebruikt:
            if calc.freeMode == True:
                data = calc.freeModeAlgorithm(sensor1, sensor2, limitSensor1, limitSensor2)
            #Als de arm in Assisted Mode staat word het algoritme daarvoor gebruikt:
            else:
                data = calc.assistedAlgorithm(sensor1, sensor2, limitSensor1, limitSensor2)
        #Bij een fout in de berekening word de arm niet bewogen en stuurt het een error terug:
        except Exception as e:
            print(e)
            calc.freeMode = True
            data = "0-0-1"
        #Plaatst de instructies op een topic om vervolgens naar de arm gestuurd te worden:
        pub.publish(data)

#Ontvangt messages van het topic 'sensordata' en regelt communicatie binnen ROS:
def controller():
    ros.init_node('decisions')
    ros.Subscriber('sensordata', String, callback)

    ros.spin()

if __name__ == '__main__':
    controller()