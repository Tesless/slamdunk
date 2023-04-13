from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

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
            </body>
        </html>
    """

@app.post("/start")
async def start_simulation(request: Request):
    subprocess.call(["roslaunch", "turtlebot3_gazebo", "turtlebot3_world.launch"])
    return {"status": "success", "message": "Turtlebot3 Gazebo simulation started."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
