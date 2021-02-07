import rospy as ros
import sys
import copy
import moveit_commander as mvit
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from moveit_commander.conversions import pose_to_list
from std_msgs.msg import String
from tf import TransformBroadcaster
from visualization_msgs.msg import *
from rospy import Time
import tkinter as tk

msg = String()
msg.data = "0-0-0-0-0"
instruction = ""
stop = False
go = True

def emergencyStop():
    global stop
    stop != stop

def getNextGoal(current_joint_value, movement, direction):
    movementInRadian = (pi/180) * movement
    if direction == 1:
        value = current_joint_value + movementInRadian
        if value > 2:
            value = 2
    else:
        value = current_joint_value - movementInRadian
        if value < 0:
            value = 0
    return value

def callback(data):
    global instruction
    global go
    instruction = data.data
    ros.loginfo(data)
    movement, direction, error = str(instruction).split('-')
    movement, direction, error = float(movement), int(direction), int(error)
    if error == 1:
        return
        
    nextValue = getNextGoal(group.get_current_joint_values()[0], movement, direction)
    print(nextValue)
    joint_goal = group.get_current_joint_values()
    joint_goal[0] = nextValue
    group.go(joint_goal, wait = True)
    go = True
    

def controller():
    global stop
    global go
    master = tk.Tk()
    slider1 = tk.Scale(master, from_=0, to=1024, orient=tk.HORIZONTAL)
    slider1.pack()
    slider2 = tk.Scale(master, from_=0, to=1024, orient=tk.HORIZONTAL)
    slider2.pack()
    button = tk.Button(master, text='Emergency stop', command=emergencyStop)
    button.pack()
    muscleSensor1, muscleSensor2, limitSensor1, limitSensor2 = 0, 0, 0, 0
    while not ros.is_shutdown():
        while go == False:
            master.update()
            pass
        if stop == True:
            msg.data = "0-0-0-0-1"
            pub.publish(msg)
        else:    
            limitSensor1 = 0
            limitSensor2 = 0
            muscleSensor1 = slider1.get()
            muscleSensor2 = slider2.get()
            if group.get_current_joint_values()[0] >= 1.99:
                limitSensor2 = 1
            if group.get_current_joint_values()[0] <= 0.0:
                limitSensor1 = 1
            dataString = str(muscleSensor1) + "-" + str(muscleSensor2) + "-" + str(limitSensor1) + "-" + str(limitSensor2) + "-0"
            msg.data = dataString
            pub.publish(msg)
        master.update()
        rate.sleep()
        go = False
    group.stop()

if __name__ == '__main__':
    mvit.roscpp_initialize(sys.argv)
    ros.Subscriber('instructions', String, callback)
    pub = ros.Publisher('sensordata', String, queue_size=10)
    ros.init_node('simulation')
    rate = ros.Rate(1)
    robot = mvit.RobotCommander()
    scene = mvit.PlanningSceneInterface()
    group_name = "arm"
    group = mvit.MoveGroupCommander(group_name)
    display_trajectory_publisher = ros.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)    
    controller()