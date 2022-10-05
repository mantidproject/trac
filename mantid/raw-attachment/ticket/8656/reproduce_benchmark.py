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
        
        Load(Filename=workspace_nexus_file,OutputWorkspace=workspace_name)
        X=mtd[workspace_name]
        
	# Run once to get a lambda workspace for alignment-calibration
	results = ReflectometryReductionOneAuto(InputWorkspace=X, ThetaIn=0.4903, I0MonitorIndex=2, AnalysisMode='MultiDetectorAnalysis',CorrectDetectorPositions=False,
	                                                                ProcessingInstructions='3:245', OutputWorkspaceWavelength='reduced_lam', WavelengthMin=0.8, WavelengthMax=14.5,
									MonitorBackgroundWavelengthMin=13, MonitorBackgroundWavelengthMax=14.5, MonitorIntegrationWavelengthMin=4, MonitorIntegrationWavelengthMax=10
									)
	
	
	reduced_lam_for_calibration = mtd['reduced_lam'][0]
	
	# Automatically determine the spectrum of interest.
        FindReflectometryLines(InputWorkspace=reduced_lam_for_calibration, StartWavelength=10, OutputWorkspace='spectrum_numbers')
        spectrum_table = mtd['spectrum_numbers']
	SC = spectrum_table.cell(0, 0)
	avgDB = spectrum_table.cell(0, 1)
	
	
        # Move the detector so that the detector channel matching the reflected beam is at 0,0
        MoveInstrumentComponent(Workspace=X,ComponentName="lineardetector",X=0,Y=0,Z=-PIX*( (SC-avgDB)/2.0 +avgDB) )
	
	# Now re-do the reduction with the components in the correct positions.
	results = ReflectometryReductionOneAuto(InputWorkspace=X, ThetaIn=0.4903, I0MonitorIndex=2, AnalysisMode='MultiDetectorAnalysis',CorrectDetectorPositions=False,
	                                                                ProcessingInstructions='3:245', OutputWorkspaceWavelength='reduced_lam', WavelengthMin=0.8, WavelengthMax=14.5,
									MonitorBackgroundWavelengthMin=13, MonitorBackgroundWavelengthMax=14.5, MonitorIntegrationWavelengthMin=4, MonitorIntegrationWavelengthMax=10
									)
	
	
        # Should now have signed theta vs Lambda
	reduced_lam = mtd['reduced_lam']
        reduced_lam_signed_theta =ConvertSpectrumAxis(InputWorkspace=reduced_lam,Target='signed_theta')
        
        # MD transformations
        ConvertToReflectometryQ(InputWorkspace=reduced_lam_signed_theta,OutputWorkspace='QxQy',OutputDimensions='Q (lab frame)', Extents='-0.0005,0.0005,0,0.12')
        
        plotSlice('QxQy',colorscalelog=True, colormax=1e9, colormin=1e1)
        
test = ReflectometryISIS()
test.runTest()