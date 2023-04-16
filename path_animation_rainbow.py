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
        self.scenario_name = 'campus'  # 'campus'
        self._line_color = 'royalblue'
        self.insertation_num = 3 # numbers of insteration 
        self.path_alpha = 0.6
        self.checkpoint_alpha = 1
        
        self.present_checkpoints = True


        if self.scenario_name == 'park':
            # park
            self._bounding_coordinates = [113.9345,22.4904,114.0001,22.5245]
            self._size = [1280, 960]
        else:
            # campus
            self._bounding_coordinates = [113.9848,22.5958,114.0048,22.6062]
            self._size = [1280, 960]

        self.img_point_list = self.generate_points()
        self.frame = len(self.img_point_list)


        self.check_point_list = self.get_checkpoints()

        

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
        point_path = f'{self.scenario_name}_data_pkl.pkl'
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

        img_point_list = self.insert(img_point_list)
        img_point_list = np.array(img_point_list)
        return img_point_list

    def get_checkpoints(self):
        point_path = f'{self.scenario_name}_wgs84_waypoints.pkl'
        
        image = plt.imread(os.path.join(
            'background', f'{self.scenario_name}_background.jpg'))
        
        with open(os.path.join('checkpoints', point_path), 'rb') as f:
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


    def scatter_animation(self,i):

        print(str(100*i/a.img_point_list.size) + '%' + ' completed')
        areas = 35 * np.ones((i,))
        colors = np.arange(0, i, 1)
        scat = ax.scatter(a.img_point_list[0:i, 0], a.img_point_list[0:i, 1], s=areas, c = colors, cmap='hsv',
                 linewidths=.4, marker='o', alpha=self.path_alpha, zorder=10)
        return scat,

    def init_scatter(self):
        # creating an empty plot/frame
        scat = ax.scatter([],[],
                 linewidths=.4, marker='o', alpha=self.path_alpha, zorder=10)
        return scat,

    def insert(self,input_list):
        output_list=[]
        for i in range(len(input_list)-1):
            output_list.append(input_list[i])
            output_list.append((input_list[i]+input_list[i+1])/2)
        output_list.append(input_list[-1])
        return output_list            


if __name__ == '__main__':

    a = AnimationGenerator()

    
    image = plt.imread(os.path.join(
        'background', f'{a.scenario_name}_background.jpg'))
    
    fig = plt.figure(figsize=[13.312,7.48799999])
    # fig = plt.figure()
    
    ax = fig.subplots()
    ax.imshow(image)
    ax.set_axis_off()

    # areas = 70 * np.ones((a.img_point_list.shape[0],))
    # colors = np.arange(a.img_point_list.shape[0], 0, -1)

    scat = ax.scatter([],[],
                 linewidths=.4, marker='o', alpha=.75, zorder=10)

    areas = 140 * np.ones((a.check_point_list.shape[0],))

    if a.present_checkpoints:
        ax.scatter(a.check_point_list[:, 0], a.check_point_list[:, 1], s=areas, c = 'royalblue',
                     linewidths=.8, marker='o', alpha=a.checkpoint_alpha, zorder=10)


    line, = ax.plot([], [], lw=2)
    plt.axis('off')
    plt.tight_layout(pad=0)
    

    # call the animator
    
    # anim = animation.FuncAnimation(fig, a.animate, init_func=a.init,
                                #    frames=a.frame, blit=True)

    anim = animation.FuncAnimation(fig, a.scatter_animation,init_func=a.init_scatter,
                                   frames=a.frame, blit=True)

    
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

