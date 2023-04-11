from fastapi import FastAPI
import rospy
import actionlib
from smach import State, StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

app = FastAPI()

class Waypoint(State):
    def __init__(self, position, orientation):
        State.__init__(self, outcomes=['success'])

        # Get an action client
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

        # Define the goal
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]

    def execute(self, userdata):
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        return 'success'

class Stop(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])

        # Get the action client
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    def execute(self, userdata):
        # Cancel the current goal
        self.client.cancel_goal()
        return 'success'

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/patrol")
async def execute_patrol():
    waypoints = [
        ['one', (1.1, 1.2), (0.0, 0.0, 0.0, 1.0)],
        ['two', (2.1, 4.43), (0.0, 0.0, -0.984047240305, 0.177907360295)],
        ['three', (-1.3, 4.4), (0.0, 0.0, 0.0, 1.0)],
        ['four', (-1.3, 0.1), (0.0, 0.0, 0.0, 1.0)]
    ]

    patrol = StateMachine(['succeeded', 'aborted', 'preempted'])
    with patrol:
        # Add the waypoints as states
        for i, w in enumerate(waypoints):
            StateMachine.add(w[0], Waypoint(w[1], w[2]), transitions={'success': waypoints[(i + 1) % len(waypoints)][0]})

        # Add a stop state
        StateMachine.add('stop', Stop(), transitions={'success': 'stop'})

    # Execute the state machine
    patrol.execute()

    # Wait for keyboard input to trigger the stop state
    input("Press Enter to stop...")
    patrol.request_preempt()

    return {"status": "done"}

