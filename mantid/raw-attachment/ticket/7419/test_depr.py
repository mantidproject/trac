# Out of the box is V2

# Uncomment this for version 1
#from mantidsimple import *

# Uncomment this for version 2 
#from mantid.simpleapi import *

#suppressV1Warnings(__file__)

Load(Filename=r'CNCS_7860_event.nxs',OutputWorkspace='CNCS_7860_event')
Rebin(InputWorkspace='CNCS_7860_event',OutputWorkspace='CNCS_7860_event',
      Params='5,1,10000')
