# Load file and create input workspaces
LoadAscii(Filename="PG3_15035-3.dat", OutputWorkspace="PG3_15035", Unit="TOF")

CreateLeBailFitInput(FullprofParameterFile=r'pg3_bank3_step_b40k.irf',GenerateBraggReflections='1',
        LatticeConstant='4.1568899999999998',InstrumentParameterWorkspace='PG3_Bank3',BraggPeakParameterWorkspace='ReflectionTable')

Load(Filename="PG3_15035_BkgdParameters.nxs", OutputWorkspace="PG3_15035_BkgdParameters")

# Set up sequential refinement
RefinePowderDiffProfileSeq(
        InputWorkspace  = "PG3_15035",
        WorkspaceIndex  = 0,
        InputProfileWorkspace = "PG3_Bank3",
        InputBraggPeaksWorkspace = "ReflectionTable",
        InputBackgroundParameterWorkspace = "PG3_15035_BkgdParameters",
        StartX  = 10000.,
        EndX    = 79000.,
        FunctionOption = "Setup",
        ProfileType = "Thermal neutron Back-to-back exponential convoluted with pseudo-voigt",
        BackgroundType = "Polynomial",
        ProjectID   = "Test001")

