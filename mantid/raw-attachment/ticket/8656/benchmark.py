"""
These system tests are to verify the behaviour of the ISIS reflectometry reduction scripts
"""

from mantid.simpleapi import *



class ReflectometryISIS(object):

    def get_workspace_name(self):
	    return "POLREF4699"
      
    def runTest(self):
        
        workspace_name = self.get_workspace_name()
        workspace_nexus_file = workspace_name + ".nxs"
        
        PIX=1.1E-3 #m
        SC=75
        avgDB=29
        Load(Filename=workspace_nexus_file,OutputWorkspace=workspace_name)
        X=mtd[workspace_name]
        X = ConvertUnits(InputWorkspace=X,Target="Wavelength",AlignBins="1")
        # Reference intensity to normalise by
        CropWorkspace(InputWorkspace=X,OutputWorkspace='Io',XMin=0.8,XMax=14.5,StartWorkspaceIndex=2,EndWorkspaceIndex=2)
        # Crop out transmission and noisy data 
        CropWorkspace(InputWorkspace=X,OutputWorkspace='D',XMin=0.8,XMax=14.5,StartWorkspaceIndex=3)
        Io=mtd['Io']
        D=mtd['D']
    
        # Peform the normaisation step
        I = D/Io 
        
        # Move the detector so that the detector channel matching the reflected beam is at 0,0
        MoveInstrumentComponent(Workspace=I,ComponentName="lineardetector",X=0,Y=0,Z=-PIX*( (SC-avgDB)/2.0 +avgDB) )
        
        # Should now have signed theta vs Lambda
        ConvertSpectrumAxis(InputWorkspace=I,OutputWorkspace='SignedTheta_vs_Wavelength',Target='signed_theta')
        
        # MD transformations
        ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='QxQy',OutputDimensions='Q (lab frame)', Extents='-0.0005,0.0005,0,0.12')
        
        plotSlice('QxQy',colorscalelog=True, colormax=1e9, colormin=1e1)
        
test = ReflectometryISIS()
test.runTest()