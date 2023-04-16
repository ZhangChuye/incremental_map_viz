import rosbag
import pickle
import os


scenario_name = 'campus'

if scenario_name == 'park':
    bag = rosbag.Bag('2022-11-18-16-34-39.bag')
elif scenario_name == 'campus':
    bag = rosbag.Bag('2022-10-30-14-53-04.bag')


wgs84_list = []
root_path = os.path.dirname(os.path.abspath(__file__))

for topic, msg, t in bag.read_messages(topics=['/ublox_gps/fix']):
    print (type(msg))
    # print(msg.longitude)
    # print(t)
    point=[msg.latitude,msg.longitude,msg.altitude]
    wgs84_list.append(point)

print(wgs84_list)    

with open(os.path.join(root_path, 'gps_data_pkl', f'{scenario_name}_data_pkl.pkl'), 'wb') as f:
        pickle.dump(wgs84_list, f)


bag.close()