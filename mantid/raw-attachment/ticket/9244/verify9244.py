LoadEventPreNexus(EventFilename=r'/SNS/VULCAN/IPTS-7727/0/20006/preNeXus/VULCAN_20006_neutron0_event.dat',
        PulseidFilename=r'/SNS/VULCAN/IPTS-7727/0/20006/preNeXus/VULCAN_20006_pulseid0.dat',
        OutputWorkspace='V20006_PP0_LEP')
MergeLogs(Workspace='V20006_PP0_LEP',LogName1='Pixel1342177282',LogName2='Pixel1342177283',MergedLogName='PulseElectric',ResetLogValue='1')
GenerateEventsFilter(InputWorkspace='V20006_PP0_LEP',
        OutputWorkspace='V20006_PP0_LEP_Filter',
        InformationWorkspace='V20006_PP0_LEP_Info',
        FastLog=True,
	LogName='PulseElectric',MinimumLogValue='0',MaximumLogValue='1',LogValueInterval='1',
        UseParallelProcessing="Parallel", NumberOfThreads=8)
