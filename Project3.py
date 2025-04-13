import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
from water_depth_collection import Borssele1_waterDepths as water_depths


# X coordinates from the Borssele wind farm
x_coordinates = np.array([504275.70675538, 505321.42552492, 506056.49023317, 506876.70378234,
       507442.82128972, 507698.48065413, 507869.44990343, 508068.77352683,
       508268.38262535, 508411.35182144, 508639.2107794 , 508782.60292921,
       503090.93642508, 504135.52710696, 505040.92112919, 506030.66841426,
       506427.79932024, 506740.79517914, 506997.33364502, 507791.8054675 ,
       502301.22306776, 503910.75035064, 503657.81636441, 504760.2209841 ,
       505553.24233198, 505583.1705347 , 506886.44149247, 501567.69310651,
       502725.27974322, 502161.22412229, 503291.60974779, 504365.97501558,
       504084.59060105, 505867.71980133, 500805.67571976, 501257.85870299,
       502444.68453643, 502473.50346598, 504792.87312848, 499930.2908757 ,
       499139.3820695 , 500664.89406448, 501145.48468111, 502530.65593533,
       503859.60065127, 498263.32667598, 499591.19299797])
# Y coordinates from the Borssele wind farm

y_coordinates = np.array([5738856.34475316, 5737281.03568837, 5736268.21864853,
       5735170.98825808, 5734242.22896508, 5733284.80057626,
       5732327.0309002 , 5731340.95300192, 5730270.02554236,
       5729283.53816111, 5728268.61794782, 5727112.42685172,
       5738377.01238587, 5737758.49573925, 5735534.94639999,
       5734268.58895612, 5732916.66575535, 5731226.22680189,
       5729647.8399564 , 5727703.14317827, 5737391.30064173,
       5736519.56075677, 5734942.29121353, 5733788.32147507,
       5731788.43069469, 5730266.33659951, 5728040.37183885,
       5736433.75890291, 5736124.50884345, 5734772.37422876,
       5733533.56983066, 5732407.30226342, 5730997.82437588,
       5728631.31665208, 5735391.6837598 , 5733701.70281136,
       5732575.05491133, 5731391.37685884, 5729137.77714593,
       5734208.59004678, 5733278.99032277, 5732377.31614806,
       5730968.16136364, 5730207.49282441, 5729531.68737784,
       5732152.02162783, 5731559.94867748])


def plot_water_depth(water_depth, x_coordinates, y_coordinates):

    """
    This function plots a grid colored water depth map.
     water_depth (float): array with water depth values.

    """
# Defines the geographic extent from wind farm coordinates
    min_x, max_x = x_coordinates.min(), x_coordinates.max()
    min_y, max_y = y_coordinates.min(), y_coordinates.max()

    x_margin = (max_x - min_x) * 0.05
    y_margin = (max_y - min_y) * 0.05



#Stack your coordinates into a 2D array: one row per point
    measure_points = np.column_stack((x_coordinates, y_coordinates))
    
    # Create a high-resolution grid for interpolation
    grid_x, grid_y = np.meshgrid(np.linspace(min_x, max_x, 1000), np.linspace(min_y, max_y, 1000))
    grid_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    np.random.seed(42)  # Ensures reproducibility


    #x = np.random.uniform(0, 10, len(water_depth))  # Random x positions
    #y = np.random.uniform(0, 10, len( water_depth))  # Random y positions
    #points = np.column_stack((x, y))

    # Create a high-resolution grid for interpolation
    rbf_interpolator = RBFInterpolator(measure_points, water_depth, smoothing=0.1)
    grid_z = rbf_interpolator(grid_points).reshape(grid_x.shape)

    #grid_x, grid_y = np.meshgrid(np.linspace(0, 10, 1000), np.linspace(0, 10, 1000))
    #grid_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))

    # Interpolate using Radial Basis Function (RBF)

    # Plot the high-resolution depth map
    fig, ax = plt.subplots(figsize=(10, 8), dpi=100)  # High DPI for quality
    img = ax.imshow(grid_z, 
                    extent=(min_x, max_x, min_y, max_y), 
                    origin="lower", cmap="Blues", aspect="auto")
    cbar = plt.colorbar(img, ax=ax, label="Water Depth (m)")



    ax.set_title("Ultra High-Resolution Water Depth Map", fontsize=14)
    ax.set_xlabel("X Coordinates")
    ax.set_ylabel("Y Coordinates")





    # Overlay the coordinates of the wind farm

    # overlaying the coordinates of the wind farm 
    def borssele_coordinates(x, y):
       ax.scatter(x_coordinates, y_coordinates, 
                  marker = '*', 
                  color='blue', 
                  edgecolor='black',
                  linewidths=2,
                  s = 10,  # Size of the marker
                  zorder = 10,  #makes sure that it is on top of the "imshow"
                  clip_on=False, #makes sure that the points are not clipped by the axes, therefore all show 
                  label='Indivisual Wind Turbines'
                  )
       print('done')
    print("Depth array length:", len(water_depth))
    print("X range:", x_coordinates.min(), x_coordinates.max())
    print("Y range:", y_coordinates.min(), y_coordinates.max())

    print("Plot extent X:", min_x, "to", max_x)
    print("Plot extent Y:", min_y, "to", max_y)

    borssele_coordinates(x_coordinates, y_coordinates)
       
       #ax.scatter(borssele_coordinates[:, 0], borssele_coordinates[:, 1], marker = '*', color='red', s = 100,  label='Wind Farm Coordinates')
    ax.legend(loc = 'lower left', fontsize = 10, frameon = True, facecolor = 'white', edgecolor = 'blue')

    plt.tight_layout()

    # Save as a super high-resolution image
    plt.savefig("water_depth_map.png", dpi=1200, bbox_inches="tight")  # Maximum DPI

    plt.show()
    plt.tight_layout(pad=8.0, w_pad=2.0, h_pad=2.0)  # Adjust layout to prevent clipping of tick-labels





# Water depth data
Borssele1_waterDepths = np.array([
    -30, -33, -31, -27, -33, -35, -29, -29, -28, -31, -32, -28, -31,
    -30, -28, -29, -34, -25, -29, -31, -30, -31, -28, -29, -34, -22, -31,
    -33, -32, -32, -24, -32, -36, -29, -33, -30, -25, -30, -24, -33, -32,
    -29, -30, -33, -31, -32, -29
])

def main():
    # Code that actually runs your logic
    plot_water_depth(Borssele1_waterDepths, x_coordinates, y_coordinates)
   

if __name__ == '__main__':
    main()
