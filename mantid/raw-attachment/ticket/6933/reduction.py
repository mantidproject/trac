import sys
sys.path.append('/home/andrei/Mantid/Build/bin')
from mantid.simpleapi import *

w=Load('/home/andrei/Mantid/mantid/Test/AutoTestData/CNCS_7860_event.nxs')
 
print w.getTofMin()
print x


