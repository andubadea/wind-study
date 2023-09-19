from windrose import WindroseAxes
import windrose
import numpy as np
from scipy.stats import circmean, circstd
import os
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

#Folder
data_folder = 'data_hague_2'

# Map properties
minlon, maxlon, minlat, maxlat = (4.305, 4.325, 52.074, 52.081)

proj = ccrs.PlateCarree()
fig = plt.figure(figsize=(14, 6))
# Draw main ax on top of which we will add windroses
main_ax = fig.add_subplot(1, 1, 1, projection=proj)
main_ax.set_extent([minlon, maxlon, minlat, maxlat], crs=proj)
main_ax.gridlines(draw_labels=True)
main_ax.coastlines()
request = cimgt.OSM()
main_ax.add_image(request, 16)
figlist = []


# Data file handling
data_files = [x for x in os.listdir(data_folder) if '.txt' in x]
output_files = [x for x in data_files if 'output' in x]
rooftop_files = [x for x in data_files if 'output' not in x]

# First, lets get the average wind direction
rooftop_dirs = []
rooftop_speeds = []
rooftop_gusts = []
for rooftop_file in rooftop_files:
    with open(data_folder +'/'+rooftop_file, 'r') as f:
        contents = f.readlines()
        
    data_split = contents[0].replace('   ', ' ').replace('  ',' ').split(' ')
    rooftop_dirs.append(float(data_split[0].replace('[','')))
    rooftop_speeds.append(float(data_split[1].replace(' ','')))
    rooftop_gusts.append(float(data_split[2].replace(']','')))

avg_dir = np.average(rooftop_dirs)
avg_spd = np.average(rooftop_speeds) / 3.6 #kph to mps
avg_gust = np.average(rooftop_gusts) / 3.6 #kph to mps

print(avg_dir, avg_spd, avg_gust)

# Now let's create wind roses
for output_file in output_files:
    # Load the data
    with open(data_folder+'/'+output_file, 'r') as f:
        contents = f.readlines()
        
    # Each line is a measurement point, so let's try getting the data for this
    wind_dirs = []
    wind_spds = []
    wind_gusts = []
    
    for line in contents:
        # Get rid of the intro of the line
        line = line.split(")")[1]
        # Separate by comma
        line = line.split(',')
        # Make a dictionary out of this
        line_dict = dict()
        for entry in line:
            line_dict[entry.split(':')[0].replace("'", '').replace(' ', '')] = \
            entry.split(':')[1].replace("'", '').replace(' ', '')

        # Ignore if entry is none
        if line_dict['windDir'] != 'None' and \
            line_dict['windSpeed'].replace('\n','') != 'None' and \
                line_dict['windGust'] != 'None':
            wind_dirs.append(float(line_dict['windDir']))
            wind_spds.append(float(line_dict['windSpeed'].replace('\n','')))
            wind_gusts.append(float(line_dict['windGust']))
        
    # Create the wind rose
    ax = WindroseAxes.from_ax()
    ax.bar(wind_dirs, wind_spds, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    ax.figure.savefig('figs/' + output_file.replace('.txt', '.png'))
    
        
    # We can also extract good info by just splitting the filename
    output_file_split = output_file.split('-')
    lat = float(output_file_split[0])
    lon = float(output_file_split[1])
    date = f'{output_file_split[4]}-{output_file_split[3]}-{output_file_split[2]}'
    time = f'{output_file_split[5]}:{output_file_split[6]}:{output_file_split[7].replace(".txt","")}'
    
    print(lat, lon)
    print(np.rad2deg(circmean(np.deg2rad(wind_dirs))), np.rad2deg(circstd(np.deg2rad(wind_dirs))))
    print(np.average(wind_spds), np.std(wind_spds))
    print(max(wind_gusts))
    
    # Add the windrose
    rose = inset_axes(
                    main_ax,
                    width=1,  # size in inches
                    height=1,  # size in inches
                    loc="center",  # center bbox at given position
                    bbox_to_anchor=(lon, lat),  # position of the axe
                    bbox_transform=main_ax.transData,  # use data coordinate (not axe coordinate)
                    axes_class=windrose.WindroseAxes,  # specify the class of the axe
                    )
    rose.bar(wind_dirs, wind_spds)
    figlist.append(rose)
    
for ax in figlist:
    ax.tick_params(labelleft=False, labelbottom=False)

plt.show()