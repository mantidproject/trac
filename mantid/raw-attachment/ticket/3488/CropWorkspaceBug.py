
######################################################################
#Python Script Generated by Algorithm History Display 
######################################################################
Load(Filename='/home/dmn58364/mantidproject/svn/trunk/Test/AutoTestData/GEM38370_Focussed_Legacy.nxs',OutputWorkspace='GEM38370_Focussed_Legacy')
Fit(InputWorkspace='GEM38370_Focussed_Legacy',WorkspaceIndex='2',StartX='4.6731234866828082',EndX='5.2542372881355934',Function='name=Gaussian,Height=878.114,PeakCentre=4.93947,Sigma=0',Output='GEM38370_Focussed_Legacy')

CropWorkspace('GEM38370_Focussed_Legacy_Workspace','Calc',StartWorkspaceIndex=1,EndWorkspaceIndex=1)

ExtractSingleSpectrum('GEM38370_Focussed_Legacy_Workspace','Calc_2',1)