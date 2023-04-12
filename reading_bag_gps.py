import rosbag
import pickle
import os


bag = rosbag.Bag('2022-11-18-16-34-39.bag')
wgs84_list = []
root_path = os.path.dirname(os.path.abspath(__file__))

for topic, msg, t in bag.read_messages(topics=['/ublox_gps/fix']):
    print (type(msg))
    # print(msg.longitude)
    # print(t)
    point=[msg.latitude,msg.longitude,msg.altitude]
    wgs84_list.append(point)

print(wgs84_list)    

with open(os.path.join(root_path, 'gps_data_pkl', 'bay_data_pkl.pkl'), 'wb') as f:
        pickle.dump(wgs84_list, f)


bag.close()