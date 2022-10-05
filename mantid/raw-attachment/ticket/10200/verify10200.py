vecx = []
vecy = []
vece = []

import random
random.seed(0)
import math

x0 = 0.0
dx = 0.1
for i in xrange(100):
    x = x0 + dx * float(i)
    y = int(random.random()*5)
    y += 10. * math.exp( -(x-5.0)**2/0.4 )
    e = math.sqrt(y)
    if e < 1.:
        e = 1.
    
    vecx.append(x)
    vecy.append(y)
    vece.append(e)

ws = CreateWorkspace(DataX=vecx, DataY=vecy, DataE=vece, NSpec=1)

fitws1 = FindPeaks(InputWorkspace=ws, WorkspaceIndex=0,PeakPositions="2.17, 5.1", PeakFunction="Gaussian", BackgroundType="Linear")

fitws2 = FindPeaks(InputWorkspace=ws, WorkspaceIndex=0,PeakPositions="2.17, 5.1", PeakFunction="Gaussian", BackgroundType="Linear", MinimumPeakHeightObs=5)
