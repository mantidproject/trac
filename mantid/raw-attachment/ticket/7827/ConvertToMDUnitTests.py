SXD23767 = Load(Filename='SXD23767.raw', LoadMonitors='Exclude')

QLab=ConvertToMD( InputWorkspace=SXD23767, QDimensions="Q3D",
                    dEAnalysisMode="Elastic", QConversionScales="Q in A^-1",
   	            LorentzCorrection='1', MinValues=[-15,-15,-15], MaxValues=[15,15,15],
                    SplitInto='2', SplitThreshold='50',MaxRecursionDepth='14' )

peaks_qLab = FindPeaksMD(InputWorkspace=QLab, MaxPeaks=300, DensityThresholdFactor=10,PeakDistanceThreshold=1.0)

FindUBUsingFFT(PeaksWorkspace=peaks_qLab, MinD='3', MaxD='5',Tolerance=0.08)

IndexPeaks(PeaksWorkspace=peaks_qLab,Tolerance=0.12,RoundHKLs=1)

CopySample(InputWorkspace=peaks_qLab, OutputWorkspace=SXD23767, CopyLattice=True, CopyName=False, CopyShape=False, CopyMaterial=False,CopyEnvironment=False)

AddSampleLog(Workspace='SXD23767',LogName='phi',LogText='0',LogType='Number')
AddSampleLog(Workspace='SXD23767',LogName='chi',LogText='0',LogType='Number')
AddSampleLog(Workspace='SXD23767',LogName='omega',LogText='0',LogType='Number')
SetGoniometer(Workspace='SXD23767',Goniometers='Universal')

ConvertToMD(InputWorkspace='SXD23767',OutputWorkspace='HKL',QDimensions='Q3D',dEAnalysisMode='Elastic',Q3DFrames='HKL',QConversionScales='HKL',MinValues='-10,-10,-10',MaxValues='10,10,10')

