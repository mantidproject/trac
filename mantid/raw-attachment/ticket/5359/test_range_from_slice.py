from mantidsimple import *
######################################################################
#Python Script Generated by GeneratePythonScript Algorithm
######################################################################
CreateMDWorkspace(Dimensions='2',Extents='0,1,0,1',Names='A,B',Units='U,U',OutputWorkspace='A')
FakeMDEventData(InputWorkspace='A',PeakParams='1000,0.5,0,0.25')
SliceMD(InputWorkspace='A',AlignedDim0='A,0,1,10',AlignedDim1='B,0,1,10',OutputExtents='0,10,0,10',OutputBins='5,5',OutputWorkspace='B')

sv = plotSlice('B')
sv.setRebinMode(True, False)
print sv.getColorScaleMin()
print sv.getColorScaleMax()
sv.setColorScaleAutoFull()
print sv.getColorScaleMin()
print sv.getColorScaleMax()
