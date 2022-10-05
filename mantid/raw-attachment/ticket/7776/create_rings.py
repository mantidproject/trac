
import numpy
import math
# get an instrument
ws = Load('LOQ48098', SpectrumMin=2, SpectrumMax=16000)

# process the workspace in order to get an image with circles around the 
# defined origin (look at the resulting workspace at instrument view)
origin = V3D(0.006,0,15.15)
n = ws.blocksize()
x_pos = numpy.zeros(ws.getNumberHistograms())
y_pos = numpy.zeros(ws.getNumberHistograms())
for i in range(ws.getNumberHistograms()):	
	try:
          if ws.getDetector(i).isMonitor() : 
		ws.setY(i,numpy.zeros(n))
		continue
	  x_pos[i] = ws.getDetector(i).getPos().getX()
	  y_pos[i] = ws.getDetector(i).getPos().getY()
	  dist = ws.getDetector(i).getPos().distance(origin)
	  if (math.sin(dist*30)<0):
            ws.setY(i,numpy.zeros(n))
	  else:
	    ws.setY(i, numpy.zeros(n) + math.sin(dist*30))
	except : 
		print 'ex'
		pass


# execute the ring profile for all the image in different rings.
min_r = 0.001
max_r = 0.33
num_steps = 20
num_bins = 36
startangle = -1
y_values = list()
delta = (max_r-min_r)/num_steps
centre = [0.006,0,15.15]

for i in range(num_steps):
  aux = RingProfile(ws, centre, min_r, min_r+delta, num_bins, startangle) 
  min_r += delta
  y_values.append(numpy.copy(aux.readY(0)))
  #if you want to compensate the fact that for small rings, the numbers of 
  # detectors are smaller, uncoment this line
  #y_values.append(aux.readY(0)/((min_r+delta/2)**2))
	
# create the result output
all_rings = CreateWorkspace(aux.readX(0),numpy.concatenate(y_values),NSpec=num_steps)

