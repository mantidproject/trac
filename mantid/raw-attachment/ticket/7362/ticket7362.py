""" Main test script for ticket 7362 """ 
 
Load(Filename=r'PG3_12007_event.nxs', OutputWorkspace='PG3_12007')

FilterBadPulses(InputWorkspace='PG3_12007', OutputWorkspace='PG3_12007')

# Output 2 workspaces
AlignAndFocusPowder(InputWorkspace='PG3_12007', OutputWorkspace='PG3_12007_High', LowResTOFWorkspace="PG3_12007_Low", 
                    CalFileName=r'/SNS/PG3/2013_1_11A_CAL/PG3_ILL_d12007_2013_01_09.cal',
                    Params='-0.0004',DMin='0.1', DMax='2.2', TMax='16666.669999999998', 
                    RemovePromptPulseWidth='50', LowResRef='15000') 

EditInstrumentGeometry(Workspace="PG3_12007_High", SpectrumIDs = 1, L2 = 3.0,
                       Polar = 90.0, Azimuthal = 0.0,  DetectorIDs = 1)

EditInstrumentGeometry(Workspace="PG3_12007_Low", SpectrumIDs = 1, L2 = 3.0,
                       Polar = 90.0, Azimuthal = 0.0,  DetectorIDs = 2)

ConvertToMatrixWorkspace(InputWorkspace="PG3_12007_High", OutputWorkspace="PG3_12007_High") 
ConvertToMatrixWorkspace(InputWorkspace="PG3_12007_Low", OutputWorkspace="PG3_12007_Low") 

ConjoinWorkspaces(InputWorkspace1 = "PG3_12007_High", InputWorkspace2 = "PG3_12007_Low", CheckOverlapping=False)

