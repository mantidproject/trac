 """ Main test script for ticket 7333 """ 
 
Load(Filename=r'PG3_4844_event.nxs', OutputWorkspace='PG3_4844')

inws = mtdP[G3_4844]

FilterBadPulses(InputWorkspace='PG3_4844', OutputWorkspace='PG3_4844')

# Output 2 workspaces
AlignAndFocusPowder(InputWorkspace='PG3_4844', OutputWorkspace='PG3_4844_High', LowResTOFWorkspace="PG3_4844_Low", 
	CalFileName=r'PG3_FERNS_d4832_2011_08_24.cal', Params='-0.0004',DMin='0.1', DMax='2.2', TMax='16666.669999999998', 
	RemovePromptPulseWidth='50', LowResRef='15000') 

# 
EditInstrumentGeometry(Workspace="PG3_4844_High", SpectrumIDs = 1, L2 = 3.0,
	Polar = 90.0, Azimuthal = 0.0,  DetectorIDs = 1)

EditInstrumentGeometry(Workspace="PG3_4844_Low", SpectrumIDs = 1, L2 = 3.0,
	Polar = 90.0, Azimuthal = 0.0,  DetectorIDs = 2)

if True:
	ConvertToMatrixWorkspace(InputWorkspace="PG3_4844_High", OutputWorkspace="PG3_4844_High") 
	ConvertToMatrixWorkspace(InputWorkspace="PG3_4844_Low", OutputWorkspace="PG3_4844_Low") 

ConjoinWorkspaces(InputWorkspace1 = "PG3_4844_High", InputWorkspace2 = "PG3_4844_Low")

