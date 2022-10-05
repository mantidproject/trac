
from mantid.simpleapi import *
from isis_reflectometry import quick
reload(quick)


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
	
# Part 2b. Use the transmission run in quick.
transmission_ws = quick.make_trans_corr(transmissionRuns,10, 12, [1.5, 0.02, 17])
quick.quick(runNo, trans=transmission_ws) 
explicit = mtd['13460_IvsLam'].clone()
	
# Compare the results of part 1 and 2
plotSpectrum([implicit, explicit], [0])
	


