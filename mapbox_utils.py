import os
import pickle
import requests
import matplotlib.pyplot as plt 
import pymap3d as pm
import numpy as np

scenario_name = 'park' # 'campus'
line_color = 'royalblue'

if scenario_name == 'park':
    # park
    bounding_coordinates = [113.937,22.4868,113.9924,22.5251]
    size = [1280, 960]
else:
    # campus
    bounding_coordinates = [113.9889,22.5947,114.0003,22.6065]
    size = [800, 900]

def download_map_background():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    token = 'pk.eyJ1IjoienlxNTA3IiwiYSI6ImNsYmkzcmt6azB3N2gzcHBkbDRjbmlxbjUifQ.0iCoci93mObv1Fr55ZTieA'
    url = f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{bounding_coordinates}/{size[0]}x{size[1]}@2x?access_token={token}'

    image = requests.get(url, headers = header)
    with open(os.path.join('background', f'{scenario_name}_background.jpg'), 'wb') as f:
        f.write(image.content)
        f.close()

if __name__ == '__main__':
    #download_map_background()
    point_path = f'{scenario_name}_wgs84_waypoints.pkl'
    image = plt.imread(os.path.join('background', f'{scenario_name}_background.jpg'))

    with open(os.path.join('checkpoints', point_path), 'rb') as f:
        checkpoints_list = pickle.load(f)
    
    ref_coordniate = [bounding_coordinates[3], bounding_coordinates[0]]
    diagnal_coordinate = [bounding_coordinates[1], bounding_coordinates[2]]

    img_size = image.shape
    actual_size = np.array(pm.enu.geodetic2enu(diagnal_coordinate[0], diagnal_coordinate[1], 0.0,
                                    ref_coordniate[0], ref_coordniate[1], 0.0,
                                    ell=None, deg=True)[:-1])
    enu2img_ratio = actual_size / np.flipud(img_size)[1:]
    print(enu2img_ratio)

    img_point_list = list()
    for checkpoint in checkpoints_list[:-2]:
        enu_coord = np.array(pm.enu.geodetic2enu(checkpoint[0], checkpoint[1], 0.0,
                                    ref_coordniate[0], ref_coordniate[1], 0.0,
                                    ell=None, deg=True)[:-1])
        img_point = enu_coord / enu2img_ratio
        if len(img_point_list) == 0 or np.linalg.norm(img_point - img_point_list[-1]) >= 10:
            img_point_list.append(img_point)
    img_point_list = np.array(img_point_list)
    colors = np.arange(img_point_list.shape[0], 0, -1)
    areas = 20 * np.ones((img_point_list.shape[0],))

    fig = plt.figure(figsize=(4, 4.5))
    ax = fig.subplots()
    ax.imshow(image)
    ax.plot(img_point_list[:, 0], img_point_list[:, 1], color=line_color, linewidth=2, alpha=.8, zorder=5)
    ax.scatter(img_point_list[:, 0], img_point_list[:, 1], s=areas, c = colors, cmap='RdYlBu',
                edgecolors='k', linewidths=0.8, marker='o', alpha=.75, zorder=10)
    # ax.plot(np.array([1250, 1250 + 500/enu2img_ratio[0]]), np.array([1600, 1600]), color='w', linewidth=1, zorder=5)
    ax.set_axis_off()
    plt.tight_layout()
    # plt.savefig(os.path.join('results', f'{scenario_name}.png'), format='png', bbox_inches='tight', dpi=400, pad_inches=0.0)
    # plt.savefig(os.path.join('results', f'{scenario_name}.svg'), format='svg', bbox_inches='tight', dpi=400, pad_inches=0.0)
    plt.show()

