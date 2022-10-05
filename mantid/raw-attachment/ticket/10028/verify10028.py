correction = 'Elastic'
correction = 'None'


Load(Filename='/home/wzz/Projects/MantidTests/EventFiltering/WISH/WISH00029057.nxs', 
        OutputWorkspace='WISH00029057', LoaderName='LoadEventNexus', LoaderVersion=1)
GenerateEventsFilter(InputWorkspace='WISH00029057', 
        OutputWorkspace='Filter29057Both', InformationWorkspace='Info29057Both', FilterLogValueByChangingDirection="Both",
        FastLog=True, LogName='ADC2', MinimumLogValue=1880, MaximumLogValue=1940)
GenerateEventsFilter(InputWorkspace='WISH00029057', 
        OutputWorkspace='Filter29057Up', InformationWorkspace='Info29057Up', FilterLogValueByChangingDirection="Increase",
        FastLog=True, LogName='ADC2', MinimumLogValue=1880, MaximumLogValue=1940)
GenerateEventsFilter(InputWorkspace='WISH00029057', 
        OutputWorkspace='Filter29057Down', InformationWorkspace='Info29057Down', FilterLogValueByChangingDirection="Decrease",
        FastLog=True, LogName='ADC2', MinimumLogValue=1880, MaximumLogValue=1940)
	
FilterEvents(InputWorkspace="WISH00029057", SplitterWorkspace="Filter29057Both", OutputWorkspaceBaseName='FilterBoth', 
	InformationWorkspace="Info29057Both", CorrectionToSample= correction, FilterByPulseTime=False)  
	
bothws = mtd["FilterBoth_0"]
numboth = bothws.getNumberEvents()


FilterEvents(InputWorkspace="WISH00029057", SplitterWorkspace="Filter29057Up", OutputWorkspaceBaseName='FilterUp', 
	InformationWorkspace="Info29057Up", CorrectionToSample= correction, FilterByPulseTime=False)  
	
upws = mtd["FilterUp_0"]
numup = upws.getNumberEvents()

FilterEvents(InputWorkspace="WISH00029057", SplitterWorkspace="Filter29057Down", OutputWorkspaceBaseName='FilterDown', 
	InformationWorkspace="Info29057Down", CorrectionToSample= correction, FilterByPulseTime=False)  
	
downws = mtd["FilterDown_0"]
numdown = downws.getNumberEvents()

print  numboth , " == ", numup, " + ", numdown, " is ", numboth == numup + numdown, " with correction type ", correction