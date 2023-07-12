import meteostat
from meteostat import Point
from datetime import datetime
from datetime import timedelta
import numpy as np

lat = 52.07916
lon = 4.30818
location = Point(lat, lon, 100)

start = datetime.now() - timedelta(minutes=60)
end = datetime.now()

data = meteostat.Hourly(location, start, end)
data = data.fetch()

wind = np.array(data)[0][5:8]

# save to file
now = datetime.now()
filename = f'{lat}-{lon}-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.txt'

with open(filename, 'w') as f:
    f.write(str(wind))