import ISISCommandInterface as ici
import os
MASKFILE = FileFinder.getFullPath('MaskSANS2DReductionGUI.txt')
SYSTEMTESTPATH=os.path.abspath(os.path.join(MASKFILE,'../../../'))
# The new standard way
ici.SANS2D()
ici.MaskFile(MASKFILE)
ici.AssignSample('22048')
ici.AssignCan('22023')
ici.TransmissionSample('22041','22024')
ici.TransmissionCan('22024', '22024')

reduced = ici.WavRangeReduction()
ev_ws = RenameWorkspace(reduced, OutputWorkspace='event_mode_reduction')


# Previously: it used the LoadNexus, so, let's use it
# enforce old result.
sample = LoadNexus('22048',OutputWorkspace='22048_sans_nxs')
can = LoadNexus('22023', OutputWorkspace='22023_sans_nxs')
ici.SANS2D()
ici.MaskFile(MASKFILE)
# assign the workspace directly 
ici.AssignSample(sample, reload=False)
ici.AssignCan(can, reload=False)
ici.TransmissionSample('22041','22024')
ici.TransmissionCan('22024', '22024')

reduced = ici.WavRangeReduction()
hist_ws = RenameWorkspace(reduced, OutputWorkspace='histogram_mode_reduction')


# load the previous reduced reference result
reference = LoadNexus(os.path.join(SYSTEMTESTPATH, 'SystemTests/AnalysisTests/ReferenceResults/SANSReductionGUI.nxs'))

CheckWorkspacesMatch(hist_ws, reference, 1.0e-5,CheckAllData=True)
CheckWorkspacesMatch(ev_ws, reference, 1.0e-2,ToleranceRelErr=True,CheckAllData=True)


