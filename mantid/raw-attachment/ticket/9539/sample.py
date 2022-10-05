# Basic parameters  for  Triphylite Crystal
#Name of the workspaces to create
ws_name = "TOPAZ_3132"
filename = ws_name +"_event.nxs"
ws = LoadEventNexus(Filename=filename,FilterByTofMin=3000, FilterByTofMax=16000)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 1. Basic Reduction

# Spherical Absorption and Lorentz Corrections
ws = AnvredCorrection(InputWorkspace=ws, LinearScatteringCoef=0.451, LinearAbsorptionCoef=0.993, Radius=0.14)

# Convert to Q space
LabQ = ConvertToDiffractionMDWorkspace(InputWorkspace=ws, LorentzCorrection='0',
        OutputDimensions='Q (lab frame)', SplitInto=2, SplitThreshold=150)
        
# Find peaks
PeaksLattice = FindPeaksMD(InputWorkspace=LabQ,MaxPeaks=100)

# 3d integration to centroid peaks
PeaksLattice = CentroidPeaksMD(InputWorkspace=LabQ,
        PeakRadius=0.12, PeaksWorkspace=PeaksLattice)
        
# Find the UB matrix using the peaks and known lattice parameters
FindUBUsingLatticeParameters(PeaksWorkspace=PeaksLattice, a=10.3522, b=6.0768, c=4.7276,
                alpha=90, beta=90, gamma=90, NumInitial=20, Tolerance=0.12)
                
# And index to HKL            
IndexPeaks(PeaksWorkspace=PeaksLattice, Tolerance=0.12)


PeaksLattice_Integrated_Clusters, ClusterImages = IntegratePeaksHybrid(InputWorkspace=LabQ, PeaksWorkspace=PeaksLattice, BackgroundOuterRadius=0.4)

svw = plotSlice(ClusterImage)
sv = svw.getSlicer()
pp_all = sv.setPeaksWorkspaces([PeaksLattice_Integrated_Clusters,PeaksLattice_Integrated])
pp = pp_all.getPeaksPresenter(PeaksLattice_Integrated_Clusters)