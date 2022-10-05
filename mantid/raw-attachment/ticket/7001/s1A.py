# determine where to save
import os
savedir = os.path.abspath(os.path.curdir)

# run the actual code
CalibrateRectangularDetectors(OutputDirectory = savedir, SaveAs = 'calibration', FilterBadPulses = True,
                  GroupDetectorsBy = 'All', DiffractionFocusWorkspace = False, Binning = '0.5, -0.0004, 2.5',
                  MaxOffset=0.01, PeakPositions = '2.0592,1.2610,1.0754,0.7280',
                  CrossCorrelation = False, Instrument = 'PG3', RunNumber = '2538', Extension = '_event.nxs')

