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
Rebin(InputWorkspace="PG3_RAW_Q",OutputWorkspace="PG3_RAW_Q",Params="1,1,40")

preserveevents = True

# 2D version
# CreateGroupingWorkspace(InstrumentName="PG3",GroupNames="bank124,bank144,bank164,bank184",OutputWorkspace="pg3_group") 
ConvertToMatrixWorkspace(InputWorkspace="PG3_RAW_Q",OutputWorkspace="PG3_RAW_Q_2D")
ConvertUnits(InputWorkspace="PG3_RAW_Q_2D", OutputWorkspace="PG3_RAW_D_2D",Target="dSpacing")
DiffractionFocussing(InputWorkspace="PG3_RAW_D_2D",OutputWorkspace="PG3_2D_FOC_D",GroupingWorkspace="PG3_group", 
        PreserveEvents=preserveevents)
ConvertUnits(InputWorkspace="PG3_2D_FOC_D", OutputWorkspace="PG3_2D_FOC_Q",Target="MomentumTransfer")
Rebin(InputWorkspace="PG3_2D_FOC_Q",OutputWorkspace="PG3_2D_FOC_Q",Params="1,1,40")

# Event version
ConvertUnits(InputWorkspace="PG3_RAW_Q", OutputWorkspace="PG3_RAW_D",Target="dSpacing")
DiffractionFocussing(InputWorkspace="PG3_RAW_D",OutputWorkspace="PG3_EVENT_FOC_D",GroupingWorkspace="PG3_group",
        PreserveEvents=preserveevents)
ConvertUnits(InputWorkspace="PG3_EVENT_FOC_D", OutputWorkspace="PG3_EVENT_FOC_Q",Target="MomentumTransfer")
Rebin(InputWorkspace="PG3_EVENT_FOC_Q",OutputWorkspace="PG3_EVENT_FOC_Q",Params="1,1,40")

Minus("PG3_EVENT_FOC_Q", "PG3_2D_FOC_Q", "PG3_diff")
