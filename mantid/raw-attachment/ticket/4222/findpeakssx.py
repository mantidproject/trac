
vanadium_raw_file = "WISH00018589.RAW"
sample_raw_file = "WISH00017986.RAW"

#load workspaces
LoadRaw(Filename=vanadium_raw_file, OutputWorkspace="vanadium");
SmoothNeighbours(InputWorkspace="vanadium", OutputWorkspace="smoothed_vanadium",Radius=3,WeightedSum='Flat',NumberOfNeighbours=35)
DeleteWorkspace(Workspace='vanadium')

LoadRaw(Filename=sample_raw_file, OutputWorkspace="sample");
SmoothNeighbours(InputWorkspace="sample", OutputWorkspace="smoothed_sample",Radius=3,WeightedSum='Flat',NumberOfNeighbours=35)
DeleteWorkspace(Workspace='sample')

SmoothData(InputWorkspace="smoothed_vanadium", OutputWorkspace="smoothed_vanadium",NPoints=50);

Divide(LHSWorkspace="smoothed_sample", RHSWorkspace="smoothed_vanadium",OutputWorkspace="normalised_sample");

DeleteWorkspace(Workspace='smoothed_vanadium')
DeleteWorkspace(Workspace='smoothed_sample')

ReplaceSpecialValues(InputWorkspace='normalised_sample',OutputWorkspace='normalised_sample',NaNValue='0',InfinityValue='10000',InfinityError='10000',BigNumberThreshold='10000',BigNumberValue='10000',BigNumberError='10000')
FindSXPeaks(InputWorkspace='product',SignalBackground='100',Resolution='0.20000000000000001',OutputWorkspace='csp79590_1_peaks')

