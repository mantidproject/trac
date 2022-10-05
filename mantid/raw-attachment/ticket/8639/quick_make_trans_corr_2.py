
from mantid.simpleapi import *
from isis_reflectometry import quick
reload(quick)

class ReflectometryQuick(object):
  
    def runTest(self):
	    
	config['default.instrument'] = 'INTER'
        LoadISISNexus(Filename='13463', OutputWorkspace='13463')
        LoadISISNexus(Filename='13464', OutputWorkspace='13464')
        LoadISISNexus(Filename='13460', OutputWorkspace='13460')
    
        transmissionRuns = '13463,13464'
        runNo = '13460'
        incidentAngle = 0.7
	
	# Part 1. Create Transmission runs implicitly as well as performing conversion.
        quick.quick(runNo, trans=transmissionRuns) 
	implicit = mtd['13460_IvsLam'].clone()
	
	# Part 2a. Create the transmission run alone.
	transmission = CreateTransmissionWorkspace(WavelengthMin=1.0, WavelengthMax=17.0, WavelengthStep=0.05, MonitorBackgroundWavelengthMin=15.0, 
	MonitorBackgroundWavelengthMax=17.0, I0MonitorIndex=2, MonitorIntegrationWavelengthMin=4.0, MonitorIntegrationWavelengthMax=10.0, 
	WorkspaceIndexList=[3,4], Params=[1.5, 0.02, 17], StartOverlap=10.0, EndOverlap=12.0, FirstTransmissionRun='13463', SecondTransmissionRun='13464')
	
	# Part 2b. Use the transmission run in quick.
	quick.quick(runNo, trans=transmission) 
	explicit = mtd['13460_IvsLam'].clone()
	
	#  Part 3. Compare results
	plotSpectrum([implicit, explicit], [0])
	
	
	
test = ReflectometryQuick()
test.runTest()


