######################################################################
#Python Script Generated by GeneratePythonScript Algorithm
######################################################################
import mantid.simpleapi as api 

# 1. Load event Nexus
Load(Filename=r'/SNS/VULCAN/IPTS-7727/0/20002/NeXus/VULCAN_20002_event.nxs',OutputWorkspace='VULCAN_20002_event')

# 2. Create correction table
api.CreateLogTimeCorrection(InputWorkspace='VULCAN_20002_event',OutputWorkspace='VULCAN_Correction')

# 3. Generate event filters by log "Special1_0" (electric field).  There are 2 log values of this log, 2 and 3. 
api.GenerateEventsFilter(InputWorkspace='VULCAN_20002_event',OutputWorkspace='VULCAN_20002_EField_Filter',InformationWorkspace='VULCAN_20002_EField_Info',LogName='Special1_0',MinimumLogValue='1.99',MaximumLogValue='3.0099999999999998',LogValueInterval='0.59999999999999998')

# 4. Filter events using correction table
api.FilterEvents(InputWorkspace='VULCAN_20002_event',
        OutputWorkspaceBaseName='VULCAN_20002_Splitted',
        InformationWorkspace='VULCAN_20002_EField_Info',
        SplitterWorkspace='VULCAN_20002_EField_Filter',
        DetectorTOFCorrectionWorkspace='VULCAN_Correction',
        GroupWorkspaces='1')

# 5. Filter events without correction 
api.FilterEvents(InputWorkspace='VULCAN_20002_event',
        OutputWorkspaceBaseName='VULCAN_20002_NoCorrection',
        InformationWorkspace='VULCAN_20002_EField_Info',
        SplitterWorkspace='VULCAN_20002_EField_Filter',
        GroupWorkspaces='1')
