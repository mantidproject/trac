wsname = "NOM_26140"
efname = "NOM_26140_event.nxs"
peaks = '0.8920,1.0758,1.2615,2.0599'
minpeakheight = 5

############################################################################
# Generate a fit window table workspace 
############################################################################

numspec = 101376
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

############################################################################
# Create a workspace for resolution 
############################################################################
Load(Filename = "NOM_26140_event.nxs", OutputWorkspace = "TempWS")
EstimatePDDetectorResolution(
        InputWorkspace = "TempWS",
        OutputWorkspace = "NOM_Estimated_ResolutionWS",
        DeltaTOF = 40.)
DeleteWorkspace(Workspace = "TempWS")

############################################################################
# Calibreate rectangular detectors 
############################################################################
CalibrateRectangularDetectors(
        Instrument = "NOM",
        RunNumber = 26140,
        Extension = "_event.nxs",
        MaxOffset = 1.,
	CrossCorrelation = False,
        PeakPositions = peaks,
        MinimumPeakHeight = minpeakheight, 
        FitwindowTableWorkspace = "NOM_26140_Window",
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        Binning = "0.5, -0.005, 5.",
        FilterBadPulses = True,
        SaveAs = "calibration",
        OutputDirectory = "/tmp/",
        DetectorResolutionWorkspace = "NOM_Estimated_ResolutionWS",
        AllowedResRange = "0.25, 4.0")
