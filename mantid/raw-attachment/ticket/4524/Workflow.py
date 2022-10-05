# Basic parameters
filename = "TOPAZ_3131_event.nxs"
#Name of the workspaces to create
ws = "TOPAZ_3131"

# Load the original data
LoadEventNexus(Filename=filename,OutputWorkspace=ws)

# Convert to reciprocal space, in the sample frame
ConvertToDiffractionMDWorkspace(InputWorkspace=ws,OutputWorkspace=ws+'_MD',
		OutputDimensions='Q (lab frame)',LorentzCorrection='1')
		
# Find peaks
FindPeaksMD(InputWorkspace=ws+'_MD',MaxPeaks='50',OutputWorkspace=ws+'_peaks')

# Find the UB matrix using the peaks and known lattice parameters
FindUBUsingLatticeParameters(PeaksWorkspace=ws+'_peaks',a='10.3522',b='6.0768',c='4.7276',
		alpha='90',beta='90',gamma='90', NumInitial='20', Tolerance='0.12')
# And index to HKL		
IndexPeaks(PeaksWorkspace=ws+'_peaks', Tolerance='0.12')
	