from windrose import WindroseAxes
import numpy as np
import os
import matplotlib.pyplot as plt

data_files = [x for x in os.listdir('data') if '.txt' in x]
output_files = [x for x in data_files if 'output' in x]
rooftop_files = [x for x in data_files if 'output' not in x]

# First, lets get the average wind direction
rooftop_dirs = []
rooftop_speeds = []
rooftop_gusts = []
for rooftop_file in rooftop_files:
    with open(rooftop_file, 'r') as f:
        contents = f.readlines()
        
    data_split = contents[0].split('  ')
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
    with open(output_file, 'r') as f:
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
    
    