################################################################################
#
# Migrated from system test : Calibrate Rectangular Detector
#
################################################################################


def runTest():
    # determine where to save
    import os
    savedir = os.path.abspath(os.path.curdir)

    # run the actual code
    CalibrateRectangularDetectors(
            Instrument      = "PG3", 
            RunNumber       = '13428',
            Extension       = '_event.nxs',
            MaxOffset       = 0.05, 
            PeakPositions   = "0.5640, 0.6029,.6305,.6864,.7280,.8182,.8916,1.0754,1.2610,2.0592",
            PeakWindowMax   = 0.1,
            PeakFunction    = "Gaussian",
            BackgroundType  = "Flat",
            Binning         = '0.5, -0.0004, 2.5', 
            GroupDetectorsBy= "Group",
            FilterBadPulses = True, 
            SaveAs          = 'calibration', 
            OutputDirectory = savedir,
            DiffractionFocusWorkspace = False, 
            CrossCorrelation = False
            )
		      
    return

runTest()

