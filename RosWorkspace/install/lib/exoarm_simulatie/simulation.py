import rospy as ros
from std_msgs.msg import String
from tf import TransformBroadcaster
from visualization_msgs.msg import *
from rospy import Time

msg = String()
msg.data = "1000-520-0-0-0"
instruction = "";

def callback(data):
	global instruction
	instruction = data.data
	ros.loginfo(data)

def controller():
	while not ros.is_shutdown():
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
	ros.Subscriber('instructions', String, callback)
	pub = ros.Publisher('sensordata', String, queue_size=10)
	ros.init_node('simulation')
	rate = ros.Rate(20)
	controller()