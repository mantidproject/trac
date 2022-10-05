CreateMDWorkspace(Dimensions=3, Extents='-10,10,-10,10,-10,10', Names='A,B,C', Units='U,U,U', OutputWorkspace='c')
FakeMDEventData(InputWorkspace='c', PeakParams='100000,-5,0,0,1')
FakeMDEventData(InputWorkspace='c', PeakParams='100000,5,0,0,1') 
