LoadEventPreNexus(
        EventFilename = "/SNS/VULCAN/IPTS-7727/0/20002/preNexus/VULCAN_20002_neutron0_event.dat",
        PulseidFilename = "/SNS/VULCAN/IPTS-7727/0/20002/preNexus/VULCAN_20002_pulseid0.dat",
        OutputWorkspace = "V20002_PP0",
        EventNumberWorkspace = "V20002_Time_Distribution"
        )

RebinByPulseTimes(
        InputWorkspace = "V20002_PP0",
        Params = "0.033", # "0, 0.1, 100",
        OutputWorkspace = "V20002_PP0_Rebin")

SumSpectra(
        InputWorkspace = "V20002_PP0_Rebin",
        OutputWorkspace = "V20002_PP0_Rebin",
        IncludeMonitors = False)

