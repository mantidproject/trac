path = "/home/wzz/Projects/Mantid-Project/Tests/DiffractionFocussing/"

# Load data
LoadEventNexus(Filename=path+"PG3_2581_event.nxs", OutputWorkspace="PG3_RAW",CompressTolerance="0.050000000000000003")
_instrument = "PG3"
wksp = mtd["PG3_RAW"]
LoadCalFile(InputWorkspace=wksp, CalFileName=path+"PG3_FERNS_2656_2011_03_20.cal", WorkspaceName=_instrument)
CloneWorkspace(wksp, "BeforeAlignment")
AlignDetectors(InputWorkspace=wksp, OutputWorkspace=wksp, OffsetsWorkspace=_instrument + "_offsets")
CloneWorkspace(wksp, "AfterAlignment")
ConvertUnits(InputWorkspace=wksp,OutputWorkspace="PG3_RAW_Q",Target="MomentumTransfer")
Rebin(InputWorkspace="PG3_RAW_Q",OutputWorkspace="PG3_RAW_Q",Params="0,1,40")

preserveevents = True

# 2D version
# CreateGroupingWorkspace(InstrumentName="PG3",GroupNames="bank124,bank144,bank164,bank184",OutputWorkspace="pg3_group") 
ConvertToMatrixWorkspace(InputWorkspace="PG3_RAW_Q",OutputWorkspace="PG3_RAW_Q_2D")
DiffractionFocussing(InputWorkspace="PG3_RAW_Q_2D",OutputWorkspace="PG3_2D_FOC",GroupingWorkspace="PG3_group", 
        PreserveEvents=preserveevents)

# Event version
DiffractionFocussing(InputWorkspace="PG3_RAW_Q",OutputWorkspace="PG3_EVENT_FOC",GroupingWorkspace="PG3_group",
        PreserveEvents=preserveevents)

Minus("PG3_EVENT_FOC", "PG3_2D_FOC", "PG3_diff")
