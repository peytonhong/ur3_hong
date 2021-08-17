import numpy as np 
import json
from glob import glob
import matplotlib.pyplot as plt

json_path = '/home/hyosung/dataset/20210817_220238/*.json'
json_files = sorted(glob(json_path))
# print(sorted(json_files))
joint_angles = []
for json_file in json_files:
    with open(json_file) as json_file_object:
        json_data = json.load(json_file_object)
        joint_angles.append(json_data['joint_angles'])
# print(len(joint_angles))
joint_angles = np.array(joint_angles)

plt.plot(joint_angles[:,5])
plt.show()
print(joint_angles[:,5])