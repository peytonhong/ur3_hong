#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from moveit_msgs.msg import RobotState
import moveit_commander

def talker():
    pub = rospy.Publisher('/robot/joint_state', RobotState, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    robot = moveit_commander.RobotCommander()
    robot_state = RobotState()
    while not rospy.is_shutdown():
        robot_state = robot.get_current_state()
        rospy.loginfo(robot_state.joint_state.position)
        pub.publish(robot_state)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass