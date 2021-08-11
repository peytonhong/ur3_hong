#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image, JointState
from moveit_msgs.msg import RobotState
import moveit_commander
from cv_bridge import CvBridge, CvBridgeError
import cv2
import sys
import numpy as np

class DataSubscriber:

    def __init__(self):
        rospy.Subscriber('/joint_states', JointState, self.callback_joint_states)
        rospy.Subscriber('/camera1/color/image_raw', Image, self.callback_image1)
        rospy.Subscriber('/camera2/color/image_raw', Image, self.callback_image2)
        self.bridge = CvBridge()
        self.image1 = None
        self.image2 = None
        self.joint_angles = None
        self.rate = rospy.Rate(1) # 10hz   

    def callback_joint_states(self, data):
        # rospy.loginfo(data.position)
        self.joint_angles = data.position

    def callback_image1(self, data):
        try:
            self.image1 = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)


    def callback_image2(self, data):
        try:
            self.image2 = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)


    def run(self):
        try:
            # rospy.spin()
            while not rospy.is_shutdown():
                rospy.loginfo(self.joint_angles)
                # cv2.imwrite('image1.png', self.image1)
                # cv2.imwrite('image2.png', self.image2)
                
                self.rate.sleep()
        except KeyboardInterrupt:
            print("Shutting Down.")

def main(args):
    rospy.init_node('data_subscriber', anonymous=True)
    sub = DataSubscriber()
    sub.run()    

if __name__ == '__main__':
    main(sys.argv)