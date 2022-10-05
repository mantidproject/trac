def runTest():
    """ This is the script for verification
    """
    ######################################################################
    # Approach 1: Use GenerateEventsFilter/FilterEvents
    ######################################################################
    LoadEventPreNexus(EventFilename=r'/SNS/VULCAN/IPTS-7727/0/20002/preNeXus/VULCAN_20002_neutron0_event.dat',
        PulseidFilename=r'/SNS/VULCAN/IPTS-7727/0/20002/preNeXus/VULCAN_20002_pulseid0.dat',
        OutputWorkspace=r'V20002_PP0_LEP')
    MergeLogs(Workspace='V20002_PP0_LEP',LogName1='Pixel1342177282',LogName2='Pixel1342177283',MergedLogName='PulseElectric',ResetLogValue='1')
    GenerateEventsFilter(InputWorkspace='V20002_PP0_LEP',
        OutputWorkspace='V20002_PP0_LEP_Filter',
        InformationWorkspace='V20002_PP0_LEP_Info',
        FastLog='1',LogName='PulseElectric',MinimumLogValue='0',MaximumLogValue='1',LogValueInterval='1',
        UseParallelProcessing="Parallel", NumberOfThreads=16)
    FilterEvents(InputWorkspace='V20002_PP0_LEP',SplitterWorkspace='V20002_PP0_LEP_Filter',
        OutputWorkspaceBaseName='V20002_PP0_Split',InformationWorkspace='V20002_PP0_LEP_Info',
        GroupWorkspaces='1',SplitSampleLogs='0', GenerateTOFCorrection=True)

    ######################################################################
    # Approach 2: Use FilterEventsByLogValuePreNxus
    ######################################################################
    FilterEventsByLogValuePreNexus(EventFilename=r'/SNS/VULCAN/IPTS-7727/0/20002/preNeXus/VULCAN_20002_neutron0_event.dat',
        PulseidFilename=r'/SNS/VULCAN/IPTS-7727/0/20002/preNeXus/VULCAN_20002_pulseid0.dat',UseParallelProcessing='Parallel',
        OutputWorkspace='20002PP0_AB',EventLogTableWorkspace='20002SpecialPixelb',FunctionMode='Filter',PixelIDtoExamine='1342177282',
        NumberOfEventsToExamine='1',
        LogPixelIDs='1342177282,1342177283',LogPIxelTags='A,B', CorrectTOFtoSample=True)

    ######################################################################
    # Compare the result from these two different approach
    ######################################################################
    Rebin(InputWorkspace='20002PP0_AB', OutputWorkspace = '20002PP0_AB', Params = -0.001, PreserveEvents = True)
    SumSpectra(InputWorkspace = '20002PP0_AB', OutputWorkspace = '20002PP0_AB')

    Rebin(InputWorkspace = 'V20002_PP0_Split_0', OutputWorkspace = 'V20002_PP0_Split_0', Params = -0.001, PreserveEvents = True)
    SumSpectra(InputWorkspace = 'V20002_PP0_Split_0', OutputWorkspace = 'V20002_PP0_Split_0')

    diffws = Minus(LHSWorkspace = '20002PP0_AB', RHSWorkspace = 'V20002_PP0_Split_0', OutputWorkspace = 'Diff20002')

    print "Diff WS name = ", diffws.name()
    absum = 0.
    vecy = diffws.readY(0)
    for i in xrange(len(vecy)):
        absum += abs(vecy[i])

    print "Total differet counts = ", absum

runTest()        


