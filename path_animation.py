import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import pickle
import requests
import matplotlib.pyplot as plt
import pymap3d as pm
import numpy as np


class AnimationGenerator():
    def __init__(self):
        self.scenario_name = 'park'  # 'campus'
        self._line_color = 'royalblue'
        if self.scenario_name == 'park':
            # park
            self._bounding_coordinates = [113.937, 22.4868, 113.9924, 22.5251]
            self._size = [1280, 960]
        else:
            # campus
            self._bounding_coordinates = [113.9889, 22.5947, 114.0003, 22.6065]
            self._size = [800, 900]

        self.img_point_list = self.generate_points()

        

        self._point_list_x = self.img_point_list[:, 0]

        self._point_list_y = self.img_point_list[:, 1]

        self._xdata, self._ydata = [], []
        

    # initialization function
    def init(self):
        # creating an empty plot/frame
        line.set_data([], [])
        return line,

    # animation function
    def animate(self, i):
        if i >= self._point_list_x.size:
            return line,

        # img_point_list[:, 0], img_point_list[:, 1], color=line_color, linewidth=2, alpha=.8, zorder=5
        self._xdata.append(self._point_list_x[i]) 
        self._ydata.append(self._point_list_y[i]) 
        line.set_data(self._xdata, self._ydata) 
        line.set_linewidth(7)
        line.set_color(self._line_color)
        line.set_zorder(5)
        line.set_alpha(.8)
        

        return line,

    def generate_points(self):
        # point_path = f'{self.scenario_name}_wgs84_waypoints.pkl'
        point_path = 'bay_data_pkl.pkl'
        image = plt.imread(os.path.join(
            'background', f'{self.scenario_name}_background.jpg'))
        

        with open(os.path.join('gps_data_pkl', point_path), 'rb') as f:
            checkpoints_list = pickle.load(f)

        ref_coordniate = [self._bounding_coordinates[3],
                          self._bounding_coordinates[0]]
        diagnal_coordinate = [
            self._bounding_coordinates[1], self._bounding_coordinates[2]]

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
        return img_point_list


if __name__ == '__main__':

    a = AnimationGenerator()

    
    image = plt.imread(os.path.join(
        'background', f'{a.scenario_name}_background.jpg'))
    
    fig = plt.figure(figsize=[13.312,9.984])
    
    ax = fig.subplots()
    ax.imshow(image)
    ax.set_axis_off()

    areas = 70 * np.ones((a.img_point_list.shape[0],))
    colors = np.arange(a.img_point_list.shape[0], 0, -1)

    # ax.scatter(a.img_point_list[:, 0], a.img_point_list[:, 1], s=areas, c = colors, cmap='RdYlBu',
                # edgecolors='k', linewidths=.8, marker='o', alpha=.75, zorder=10)
    line, = ax.plot([], [], lw=2)
    plt.axis('off')
    plt.tight_layout(pad=0)
    

    # call the animator
    anim = animation.FuncAnimation(fig, a.animate, init_func=a.init,
                                   frames=300, blit=False)

    
    FFwriter = animation.FFMpegWriter()
    anim.save('animation_test.mp4',writer = FFwriter)
    
    

    # save the animation as mp4 video file
    # anim.save('test_animation.mp4', writer='ffmpeg', fps=60)
    # anim.save('test_animation.gif',writer='imagemagick') 
    # f = r"/home/zhang/Documents/incremental_map_viz/test_animation.mp4" 
    # writervideo = animation.FFMpegWriter(fps=60) 
    # anim.save(f, writer=writervideo)

    # TODO: change the right bage data to run to see if the imgage suits
    # TODO: the switching system is not good now, you should improve it 

