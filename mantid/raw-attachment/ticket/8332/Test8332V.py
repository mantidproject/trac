# Data
LoadAscii(Filename=r'VULCAN_22946_NOM.dat',
        OutputWorkspace='VULCAN_22946_NOM',Unit='TOF')

# Reflections and starting profile parameters
CreateLeBailFitInput(FullprofParameterFile=r'VULCAN_SNS_1.irf',
        GenerateBraggReflections='1',LatticeConstant='5.4313640000000003',InstrumentParameterWorkspace='Vulcan_B270_Profile',
        BraggPeakParameterWorkspace='GeneralReflectionTable')

# Pre-refined background
paramnames = ["Bkpos", "A0", "A1", "A2", "A3", "A4", "A5"]
paramvalues = [11000.000, 0.034, 0.027, -0.129, 0.161, -0.083, .015]
bkgdtablewsname = "VULCAN_22946_Bkgd_Parameter"
CreateEmptyTableWorkspace(OutputWorkspace=bkgdtablewsname)
ws = mtd[bkgdtablewsname]
ws.addColumn("str", "Name")
ws.addColumn("double", "Value")
for i in xrange(len(paramnames)):
    ws.addRow([paramnames[i], paramvalues[i]])

# Examine profile
ExaminePowderDiffProfile(
        InputWorkspace      = "VULCAN_22946_NOM",
        LoadData            = False,
        StartX              = 7000.,
        EndX                = 33000.,
        ProfileType         = "Back-to-back exponential convoluted with PseudoVoigt",
        ProfileWorkspace    = "Vulcan_B270_Profile",
        BraggPeakWorkspace  = "GeneralReflectionTable",
        GenerateInformationWS   = False,
        BackgroundParameterWorkspace    = "VULCAN_22946_Bkgd_Parameter",
        ProcessBackground   = False,
        BackgroundType      = "FullprofPolynomial",
        BackgroundWorkspace = "Dummy",
        OutputWorkspace     = "VULCAN_22946_Calculated")

