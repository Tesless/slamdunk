# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# import subprocess
# import psutil
# import rospy
# from std_msgs.msg import Empty

# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return """
#         <html>
#             <head>
#                 <title>ROS Turtlebot3 Control Panel</title>
#             </head>
#             <body>
#                 <h1>Welcome to ROS Turtlebot3 Control Panel</h1>
#                 <form action="/start" method="post">
#                     <button type="submit">Start Turtlebot3 Simulation</button>
#                 </form>
#                 <form action="/stop" method="post">
#                     <button type="submit">Stop Turtlebot3 Simulation</button>
#                 </form>
#             </body>
#         </html>
#     """

# # 노드 실행 함수
# def start_navigation():
#     subprocess.call(["roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch"])

# # 노드 종료 함수
# def stop_move_base():
#     subprocess.call(["rosnode", "kill", "/move_base"])

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)

# @app.post("/start")
# async def start_simulation(request: Request):
#     subprocess.call(["roslaunch", "turtlebot3_gazebo", "turtlebot3_world.launch"])
#     return {"status": "success", "message": "Turtlebot3 Gazebo simulation started."}

# # @app.post("/stop")
# # async def stop_simulation(request: Request):
# #     subprocess.call(["roslaunch", "turtlebot3_gazebo", "turtlebot3_world.launch", "gui:=false"])
# #     return {"status": "success", "message": "Turtlebot3 Gazebo simulation stopped."}

# @app.post("/stop")
# async def stop_simulation(request: Request):
#     rospy.init_node("stop_simulation")
#     pub = rospy.Publisher('/gazebo/pause_physics', Empty, queue_size=10)
#     rospy.loginfo("Pausing Gazebo physics...")
#     pub.publish(Empty())
#     return {"status": "success", "message": "Turtlebot3 Gazebo simulation stopped."}

# @app.post("/start")
# async def start_simulation(request: Request):
#      subprocess.call(["roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch"])
#      return {"status": "success", "message": "Turtlebot3 Gazebo simulation started."}

# @app.post("/stop")
# async def stop_simulation(request: Request):
#      subprocess.call(["roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch", "--args", "gui:=false"])
#   #    subprocess.call(["roslaunch", "turtlebot3_gazebo", "turtlebot3_world.launch", "gui:=false"])
#      return {"status": "success", "message": "Turtlebot3 Gazebo simulation stopped."}

# @app.post("/stop")
# async def stop_simulation(request: Request):
#      rospy.init_node("stop_simulation")
#      pub = rospy.Publisher('/gazebo/pause_physics', Empty, queue_size=10)
#      rospy.loginfo("Pausing Gazebo physics...")
#      pub.publish(Empty())
#      return {"status": "success", "message": "Turtlebot3 Gazebo simulation stopped."}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)

# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# import subprocess
# import psutil
# import rospy
# from std_msgs.msg import Empty

# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return """
#         <html>
#             <head>
#                 <title>ROS Turtlebot3 Control Panel</title>
#             </head>
#             <body>
#                 <h1>Welcome to ROS Turtlebot3 Control Panel</h1>
#                 <form action="/start" method="post">
#                     <button type="submit">Start Turtlebot3 Simulation</button>
#                 </form>
#                 <form action="/stop" method="post">
#                     <button type="submit">Stop Turtlebot3 Simulation</button>
#                 </form>
#             </body>
#         </html>
#     """

# # 노드 실행 함수
# def start_navigation():
#     subprocess.call(["roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch"])

# # 노드 종료 함수
# def stop_move_base():
#     subprocess.call(["rosnode", "kill", "/move_base"])

# @app.post("/start")
# async def start_simulation(request: Request):
#     start_navigation()
#     return {"status": "success", "message": "Turtlebot3 Navigation simulation started."}

# @app.post("/stop")
# async def stop_simulation(request: Request):
#     stop_move_base()
#     return {"status": "success", "message": "Turtlebot3 Navigation simulation stopped."}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

roslaunch_process = None  # roslaunch 실행 subprocess 객체를 저장할 변수

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return """
        <html>
            <head>
                <title>ROS Turtlebot3 Control Panel</title>
            </head>
            <body>
                <h1>Welcome to ROS Turtlebot3 Control Panel</h1>
                <form action="/start" method="post">
                    <button type="submit">Start Turtlebot3 Simulation</button>
                </form>
                <form action="/stop" method="post">
                    <button type="submit">Stop Turtlebot3 Simulation</button>
                </form>
            </body>
        </html>
    """

# 노드 실행 함수
def start_navigation():
    global roslaunch_process  # 전역 변수로 선언하여 다른 함수에서도 사용할 수 있도록 함
    roslaunch_process = subprocess.Popen(["roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch"])

# 노드 종료 함수
def stop_navigation():
    global roslaunch_process  # 전역 변수로 선언하여 다른 함수에서도 사용할 수 있도록 함
    if roslaunch_process is not None:
        roslaunch_process.send_signal(subprocess.signal.SIGINT)  # roslaunch 실행 프로세스에 강제 종료 시그널 전송
        roslaunch_process = None  # 프로세스 객체 초기화

@app.post("/start")
async def start_simulation(request: Request):
    start_navigation()
    return {"status": "success", "message": "Turtlebot3 Gazebo simulation started."}

@app.post("/stop")
async def stop_simulation(request: Request):
    stop_navigation()
    return {"status": "success", "message": "Turtlebot3 Gazebo simulation stopped."}
