import rosbag
import pickle
import os


bag = rosbag.Bag('test_gps_data.bag')
wgs84_list = []
root_path = os.path.dirname(os.path.abspath(__file__))

for topic, msg, t in bag.read_messages(topics=['/gps/fix']):
    # print (type(msg))
    # print(msg.longitude)
    point=[msg.latitude,msg.longitude,msg.altitude]
    wgs84_list.append(point)

print(wgs84_list)    

with open(os.path.join(root_path, 'gps_data_pkl', 'test.pkl'), 'wb') as f:
        pickle.dump(wgs84_list, f)


bag.close()