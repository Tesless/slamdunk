import rospy
from geometry_msgs.msg import Twist
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn

rospy.init_node('turtlebot3_control')

app = FastAPI()
templates = Jinja2Templates(directory="templates")
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
twist = Twist()

@app.get("/")
async def index(request: Request):
    twist.linear.x = 0.0
    twist.angular.z = 0.0
    pub.publish(twist)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/patrol")
async def patrol(request: Request, patrol_speed: float = Form(...), stop_patrol: bool = Form(False)):
    if stop_patrol:
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
    else:
        twist.linear.x = patrol_speed
        twist.angular.z = 0.0
        pub.publish(twist)
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__doit__":
    uvicorn.run("doit:app", host="0.0.0.0", port=8000)
