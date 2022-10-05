
import numpy as np
import math
npoints=100
x_pos = np.linspace(-10,10, npoints)
y_pos = np.linspace(-10,10, npoints)
half_bin = (x_pos[1]-x_pos[0])/2.0
x_bins = np.concatenate((x_pos - half_bin , [x_pos[-1]+half_bin]))
print x_bins.shape
y_values = np.zeros((npoints*npoints))

for iy in range(npoints):
	for ix in range(npoints):		
		distance = math.sqrt(x_pos[ix]**2+y_pos[iy]**2)
		if math.sin(distance) < 0:
			y_values[iy*npoints+ix] =  0
		else:
			y_values[iy*npoints+ix] = math.sin(distance)



vUnit = 'dSpacing'
ws = CreateWorkspace(x_bins, y_values, NSpec=npoints, VerticalAxisValues=y_pos, VerticalAxisUnit=vUnit)


# execute the ring profile for all the image in different rings.
min_r = 0.1
max_r = 12
num_steps = 20
num_bins = 36
startangle = -1
y_values = list()
delta = (max_r-min_r)/num_steps
centre = [0,0]

for i in range(num_steps):
  aux = RingProfile(ws, centre, min_r, min_r+delta, num_bins, startangle) 
  min_r += delta
  y_values.append(numpy.copy(aux.readY(0)))
  #if you want to compensate the fact that for small rings, the numbers of 
  # detectors are smaller, uncoment this line
  #y_values.append(aux.readY(0)/((min_r+delta/2)**2))
	
# create the result output
all_rings = CreateWorkspace(aux.readX(0),numpy.concatenate(y_values),NSpec=num_steps)

