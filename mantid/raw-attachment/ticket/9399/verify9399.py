wsname = "NOM_26140"
efname = "NOM_26140_event.nxs"
peaks = '0.8920,1.0758,1.2615,2.0599'
minpeakheight = 5

LoadEventNexus(Filename=efname,OutputWorkspace=wsname)
FilterBadPulses(InputWorkspace=wsname,OutputWorkspace=wsname)
CompressEvents(InputWorkspace=wsname,OutputWorkspace=wsname,Tolerance='0.01')
ConvertUnits(InputWorkspace=wsname,OutputWorkspace=wsname,Target='dSpacing')
SortEvents(InputWorkspace=wsname)
Rebin(InputWorkspace=wsname,OutputWorkspace=wsname,Params='0.5,-0.005,5')

# Make a copy
CloneWorkspace(InputWorkspace=wsname, OutputWorkspace=wsname+"_copy")

# Use non-fit-window version
GetDetOffsetsMultiPeaks(InputWorkspace=wsname,DReference=peaks,BackgroundType='Linear',
	OutputWorkspace='%soffset'%(wsname),NumberPeaksWorkspace='%speaks'%(wsname),MaskWorkspace='%smask'%(wsname),
	MinimumPeakHeight=minpeakheight,
        SpectraFitInfoTableWorkspace=wsname+"_offsetinfo_old",
        PeaksOffsetTableWorkspace=wsname+"_fitpeakinfo_old")
Rebin(InputWorkspace=wsname,OutputWorkspace=wsname,Params='0.5,-0.005,5')
ConvertUnits(InputWorkspace=wsname,OutputWorkspace=wsname,Target='TOF')
MaskDetectors(Workspace=wsname,MaskedWorkspace='%smask'%(wsname))
AlignDetectors(InputWorkspace=wsname,OutputWorkspace=wsname,OffsetsWorkspace='%soffset'%(wsname))
SortEvents(InputWorkspace=wsname)
Rebin(InputWorkspace=wsname,OutputWorkspace=wsname,Params='0.5,-0.005,5')
RenameWorkspace(InputWorkspace=wsname,OutputWorkspace='%s_calibrated_old'%(wsname))
RenameWorkspace(InputWorkspace=wsname+"mask", OutputWorkspace=wsname+"mask_old")

# Use fit window

# Generate fit window table workspace
RenameWorkspace(InputWorkspace=wsname+"_copy", OutputWorkspace=wsname)
ws = mtd[wsname]
numspec = ws.getNumberHistograms()
print "Number of histogram = ", numspec

windowws = CreateEmptyTableWorkspace(OutputWorkspace="NOM_26140_Window")

windowws.addColumn("int", "spectrum") 
windowws.addColumn("double", "peak0_left") 
windowws.addColumn("double", "peak0_right") 
windowws.addColumn("double", "peak1_left") 
windowws.addColumn("double", "peak1_right") 
windowws.addColumn("double", "peak2_left") 
windowws.addColumn("double", "peak2_right") 
windowws.addColumn("double", "peak3_left") 
windowws.addColumn("double", "peak3_right") 

# 0.892000, 1.075800, 1.261500, 2.06000

peak0left = 0.872
peak0right = 0.945

peak1left = 1.050
peak1right = 1.138

peak2left = 1.218
peak2right = 1.350

peak3left = 1.91
peak3right = 2.20

for iws in xrange(numspec):
    windowws.addRow([iws, peak0left, peak0right, peak1left, peak1right, peak2left, peak2right,
        peak3left, peak3right])

GetDetOffsetsMultiPeaks(InputWorkspace=wsname,DReference=peaks,BackgroundType='Linear',
	OutputWorkspace='%soffset'%(wsname),NumberPeaksWorkspace='%speaks'%(wsname),MaskWorkspace='%smask'%(wsname),
	MinimumPeakHeight=minpeakheight,
	FitwindowTableWorkspace = "NOM_26140_Window",
        SpectraFitInfoTableWorkspace=wsname+"_offsetinfo_new",
        PeaksOffsetTableWorkspace=wsname+"_fitpeakinfo_new")
Rebin(InputWorkspace=wsname,OutputWorkspace=wsname,Params='0.5,-0.005,5')
ConvertUnits(InputWorkspace=wsname,OutputWorkspace=wsname,Target='TOF')
MaskDetectors(Workspace=wsname,MaskedWorkspace='%smask'%(wsname))
AlignDetectors(InputWorkspace=wsname,OutputWorkspace=wsname,OffsetsWorkspace='%soffset'%(wsname))
SortEvents(InputWorkspace=wsname)
Rebin(InputWorkspace=wsname,OutputWorkspace=wsname,Params='0.5,-0.005,5')
RenameWorkspace(InputWorkspace=wsname,OutputWorkspace='%s_calibrated_new'%(wsname))
RenameWorkspace(InputWorkspace=wsname+"mask", OutputWorkspace=wsname+"mask_new")
