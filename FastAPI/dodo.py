from fastapi import FastAPI

import rospy
from geometry_msgs.msg import Twist

app = FastAPI()

rospy.init_node('turtlebot3_control')

@app.post("/move")
async def move_turtlebot3(linear_speed: float, angular_speed: float):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    twist = Twist()
    twist.linear.x = linear_speed
    twist.angular.z = angular_speed
    pub.publish(twist)
    return {"message": "Turtlebot3 moved successfully!"}


