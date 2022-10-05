######################################################################
#Python Script Generated by GeneratePythonScript Algorithm
######################################################################
######################################################################
#Python Script Generated by GeneratePythonScript Algorithm
######################################################################
LoadRaw(Filename=r'/archive/ndxwish/Instrument/data/cycle_11_3/WISH00018645.raw',OutputWorkspace='18645-raw',LoadLogFiles='0')
MaskBins(InputWorkspace='18645-raw',OutputWorkspace='18645-raw-mask',XMin='99900',XMax='106000')
ConvertUnits(InputWorkspace='18645-raw-mask',OutputWorkspace='18645-raw-mask',Target='dSpacing')
DiffractionFocussing(InputWorkspace='18645-raw-mask',OutputWorkspace='18645-raw-mask',GroupingFileName=r'/home/ryb18365/Calibration/Cycle_11_3/WISH_cycle_10_3_noends.cal')
ConvertUnits(InputWorkspace='18645-raw-mask',OutputWorkspace='18645-raw-mask',Target='TOF')

LoadEventNexus(Filename=r'/archive/ndxwish/Instrument/data/cycle_11_3/WISH00018645.nxs',OutputWorkspace='18645-nxs',LoadMonitors='1')
LoadRaw(Filename=r'/archive/ndxwish/Instrument/data/cycle_11_3/WISH00018645.raw',OutputWorkspace='18645-raw',LoadLogFiles='0')
RebinToWorkspace(WorkspaceToRebin='18645-nxs',WorkspaceToMatch='18645-raw',OutputWorkspace='18645-nxs')
MaskBins(InputWorkspace='18645-nxs',OutputWorkspace='18645-nxs',XMin='99900',XMax='106000')
ConvertUnits(InputWorkspace='18645-nxs',OutputWorkspace='18645-nxs',Target='dSpacing')
DiffractionFocussing(InputWorkspace='18645-nxs',OutputWorkspace='18645-nxs',GroupingFileName=r'/home/ryb18365/Calibration/Cycle_11_3/WISH_cycle_10_3_noends.cal')
ConvertUnits(InputWorkspace='18645-nxs',OutputWorkspace='18645-nxs',Target='TOF')
