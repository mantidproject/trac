# Basic parameters  for  Triphylite Crystal
#Name of the workspaces to create
ws = "TOPAZ_3132"
filename = ws+"_event.nxs"
LoadEventNexus(Filename=filename,OutputWorkspace=ws,FilterByTofMin='3000',FilterByTofMax='16000')

# Load optimized DetCal file
#LoadIsawDetCal(InputWorkspace=ws,Filename="/SNS/TOPAZ/shared/Spectra/TOPAZ_8Sept11.DetCal")

# Spherical Absorption and Lorentz Corrections
AnvredCorrection(InputWorkspace=ws,OutputWorkspace=ws,LinearScatteringCoef="0.451",LinearAbsorptionCoef="0.993",Radius="0.14")

# Convert to Q space
ConvertToDiffractionMDWorkspace(InputWorkspace=ws,OutputWorkspace=ws+'_MD2',LorentzCorrection='0',
        OutputDimensions='Q (lab frame)', SplitInto='2',SplitThreshold='150')
# Find peaks
FindPeaksMD(InputWorkspace=ws+'_MD2',MaxPeaks='100',OutputWorkspace=ws+'_peaksLattice')
# 3d integration to centroid peaks
CentroidPeaksMD(InputWorkspace=ws+'_MD2',CoordinatesToUse='Q (lab frame)',
	PeakRadius='0.12',PeaksWorkspace=ws+'_peaksLattice',OutputWorkspace=ws+'_peaksLattice')
# Find the UB matrix using the peaks and known lattice parameters
FindUBUsingLatticeParameters(PeaksWorkspace=ws+'_peaksLattice',a='10.3522',b='6.0768',c='4.7276',
                alpha='90',beta='90',gamma='90', NumInitial='20', Tolerance='0.12')
# And index to HKL            
IndexPeaks(PeaksWorkspace=ws+'_peaksLattice', Tolerance='0.12')
# Integrate peaks in Q space using spheres
IntegratePeaksMD(InputWorkspace=ws+'_MD2',PeakRadius='0.12',
	BackgroundOuterRadius='0.18',BackgroundInnerRadius='0.15',
	PeaksWorkspace=ws+'_peaksLattice',OutputWorkspace=ws+'_peaksNoEdge',IntegrateIfOnEdge=False)
IntegratePeaksMD(InputWorkspace=ws+'_MD2',PeakRadius='0.12',
	BackgroundOuterRadius='0.18',BackgroundInnerRadius='0.15',
	PeaksWorkspace=ws+'_peaksLattice',OutputWorkspace=ws+'_peaksEdge')
