from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from geometry_msgs.msg import Point, Twist
from nav_msgs.msg import Odometry
import rospy
from math import atan2

app = FastAPI()
templates = Jinja2Templates(directory="templates")
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

current_position = Point(0, 0, 0)  # 현재 위치를 나타내는 Point 메시지
goal_position = Point(1, 1, 0)  # 이동하려는 목표 위치를 나타내는 Point 메시지

def update_position(data):
    global current_position
    current_position = data.pose.pose.position

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/move_to_goal")
async def move_to_goal(request: Request, x: float = Form(...), y: float = Form(...)):
    global current_position, goal_position
    
    goal_position.x = x
    goal_position.y = y
    
    # 현재 위치와 목표 위치를 이용해 이동 방향과 거리를 계산
    direction = atan2(goal_position.y - current_position.y, goal_position.x - current_position.x)
    distance = ((goal_position.x - current_position.x)**2 + (goal_position.y - current_position.y)**2)**0.5
    
    # 이동 방향과 거리를 이용해 이동 속도를 계산
    linear_speed = 0.1 * distance
    angular_speed = 0.3 * (direction - current_position.z)
    
    # Twist 메시지를 만들어 이동 방향과 속도를 설정하고 /cmd_vel 토픽으로 전송
    twist = Twist()
    twist.linear.x = linear_speed
    twist.angular.z = angular_speed
    pub.publish(twist)

    # 로봇의 현재 위치를 업데이트
    rospy.Subscriber("/odom", Odometry, update_position)

    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__goalmain__':
    rospy.init_node('move_to_goal')
    rate = rospy.Rate(10)  # 루프 주기를 10Hz로 설정
    
    while not rospy.is_shutdown():
        rate.sleep()
