#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image, JointState
from moveit_msgs.msg import RobotState
from moveit_msgs.msg import MoveGroupActionFeedback
import moveit_commander
from cv_bridge import CvBridge, CvBridgeError
import cv2
import sys
import os
import numpy as np
from datetime import datetime
import json

class DataSubscriber:

    def __init__(self):
        group_name = "manipulator"
        self.group = moveit_commander.MoveGroupCommander(group_name)
        self.robot = moveit_commander.RobotCommander()
        rospy.Subscriber('/joint_states', JointState, self.callback_joint_states)
        rospy.Subscriber('/camera1/color/image_raw', Image, self.callback_image1)
        rospy.Subscriber('/camera2/color/image_raw', Image, self.callback_image2)
        rospy.Subscriber('/move_group/feedback', MoveGroupActionFeedback, self.callback_state)
        self.bridge = CvBridge()
        self.image1 = None
        self.image2 = None
        self.joint_angles = None
        self.rate = rospy.Rate(10) # 10hz   
        self.state = None
        self.data_count = 0
        self.base_dir = '/home/hyosung/dataset2/'
        self.set_dataset_directory()
        
        
        
    def set_dataset_directory(self):
        self.data_count = 0
        time = datetime.now()
        time_str = str(time.year) + str(time.month).zfill(2) + str(time.day).zfill(2) + '_' + \
                    str(time.hour).zfill(2) + str(time.minute).zfill(2) + str(time.second).zfill(2)
        
        self.dataset_dir = self.base_dir + time_str
        os.mkdir(self.dataset_dir)
        os.mkdir(self.dataset_dir + '/cam1')
        os.mkdir(self.dataset_dir + '/cam2')
        

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

    def callback_state(self, data):
        self.state = data.feedback.state

    def run(self):
        try:
            # rospy.spin()
            while not rospy.is_shutdown():
                # if not self.joint_angles is None:
                #     rospy.loginfo(self.joint_angles) # THIS DOES NOT LOOK ACCURATE
                
                if self.state == "MONITOR": # Robot in motion
                    json_path   = self.dataset_dir + '/' + str(self.data_count).zfill(4) + '.json'
                    image1_path = self.dataset_dir + '/cam1/' + str(self.data_count).zfill(4) + '.jpg'
                    image2_path = self.dataset_dir + '/cam2/' + str(self.data_count).zfill(4) + '.jpg'
                    cv2.imwrite(image1_path, self.image1, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
                    cv2.imwrite(image2_path, self.image2, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
                    # print(self.robot.get_current_state().joint_state.position)  ##### This has litte error
                    print(self.group.get_current_joint_values())   ############### compare both variables
                    # print(self.joint_angles)   ##### This is incorrect
                    annotation = {'joint_angles': self.group.get_current_joint_values()}                     
                    with open(json_path, 'w') as json_file:
                        json.dump(annotation, json_file)
                    self.data_count += 1

                    if self.data_count >= 5000:
                        self.set_dataset_directory()
                self.rate.sleep()

        except KeyboardInterrupt:
            print("Shutting Down.")

def main(args):
    rospy.init_node('data_subscriber', anonymous=True)
    sub = DataSubscriber()
    sub.run()    
    # rospy.spin()

if __name__ == '__main__':
    main(sys.argv)