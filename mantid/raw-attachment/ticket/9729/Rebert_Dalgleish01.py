import numpy as np
#import matplotlib.pyplot as plt
from tube import calibrate
from tube_spec import TubeSpec

#high intensity Version 30x30mm beam
w258=Load("258")
for i in range(259,266):
	        print i
                wtemp=Load(str(i))
                w258=w258+wtemp

w258int=Integration(w258,20000.0,100000.0)
ws2=Integration(w258,45000.0,100000.0)

known_pos1 = np.array([-0.297,-0.2,-0.1,0.0,0.1,0.2])
known_pos1 = known_pos1 +(0.6165-0.571)
print known_pos1

peaks_form1 = 6*[1] # all the peaks are gaussian peaks
tubes1=['LARMOR/LARMORSANSDetector/tube%d'%(i) for i in range(1,81)]
print tubes1

calibrationTable = calibrate(ws2,tubes1,known_pos1, peaks_form1,margin=20)


