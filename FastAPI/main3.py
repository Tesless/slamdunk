#!/usr/bin/env python

import rospy
import actionlib
import sys
import threading
import time

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

def stop():
    ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    input_val = ''
    ac.wait_for_result()
    finished_before_timeout = ac.wait_for_result(rospy.Duration(0.1))
    print("Stop : Press 'S' : ")
    input_val = raw_input()
    if input_val == 'S':
        ac.cancel_goal()

def goal():
    ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Waiting for action server to start.")
    ac.wait_for_server()
    rospy.loginfo("Action server started, sending goal.")
    
    x = 1.7
    y = 0.2
    
    while not rospy.is_shutdown():
        input_val = raw_input("Current goal: A\nPress 'A' to stay at A 눌러보세요 여러분 A, B, C, D : ")
        if input_val == 'A':
            x = 1.7
            y = 0.2
        elif input_val == 'B':
            x = 1.7
            y = 4.8
        elif input_val == 'C':
            x = -1.3
            y = 3.7
        elif input_val == 'D':
            x = -1.3
            y = 0.1
        elif input_val == 'S':
            time.sleep(10)
            continue

        goal = MoveBaseGoal()
        goal.target_pose.header.seq = 0
        goal.target_pose.header.stamp.secs = 0
        goal.target_pose.header.stamp.nsecs = 0
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.025547
        goal.target_pose.pose.orientation.w = 0.98381429

        ac.send_goal(goal)

        print("Stop : Press 'S' : ")
        input_val = raw_input()
        if input_val == 'S':
            ac.cancel_goal()

        ac.wait_for_result(rospy.Duration(30.0))
        if ac.get_state() == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("Succeeded!")
        else:
            rospy.logwarn("Failed!")

if __name__ == '__main3__':
    rospy.init_node('A_B_action_client')
    t1 = threading.Thread(target=goal)
    # t2 = threading.Thread(target=stop)

    t1.start()
    # t2.start()

    t1.join()
    # t2.join()
