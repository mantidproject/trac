## 
## Testing ConvertToMD
##
fake_data = CreateSimulationWorkspace(Instrument='MERLIN',BinParams=[-30,3,279],UnitX='DeltaE', DetectorTableFilename='MER06398.raw')
AddSampleLog(Workspace=fake_data, LogName='Ei',LogText=str(300), LogType="Number")

ConvertToMDEvents(InputWorkspace='fake_data',OutputWorkspace='fake_md',QDimensions='Q3D',QConversionScales='HKL',MinValues='-15,-15,-15,-15',MaxValues='25,25,25,279')
DeleteWorkspace('fake_md')

ConvertToMD(InputWorkspace='fake_data',OutputWorkspace='fake_md',QDimensions='Q3D',QConversionScales='HKL',MinValues='-15,-15,-15,-15',MaxValues='25,25,25,279')
