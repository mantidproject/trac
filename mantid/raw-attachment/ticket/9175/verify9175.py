LoadCalFile(InstrumentName="POWGEN", CalFilename="PG3_JANIShighT_d17932_2014_03_12.cal", WorkspaceName="PG3")
LoadMask(Instrument="POWGEN", InputFile="Mask-19884.xml", OutputWorkspace="other_mask")
BinaryOperateMasks(InputWorkspace1="PG3_mask", InputWorkspace2="other_mask", OperationType='OR', OutputWorkspace="new_mask")
SaveCalFile(GroupingWorkspace="PG3_group", OffsetsWorkspace="PG3_offsets", MaskWorkspace="new_mask", Filename="/tmp/deleteme.cal")