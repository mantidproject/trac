SXD23767 = Load(Filename='SXD23767.raw', LoadMonitors='Exclude')
NaCl_no_split =ConvertToMD( InputWorkspace=SXD23767,  QDimensions="Q3D",
                    dEAnalysisMode="Elastic", QConversionScales="Q in A^-1",
                    LorentzCorrection='1', MinValues=[-15,-15,-15], MaxValues=[15,15,15],
                    SplitInto='2', SplitThreshold='500',MaxRecursionDepth='14' )

NaCl_split = ConvertToMD( InputWorkspace=SXD23767, QDimensions="Q3D",
                    dEAnalysisMode="Elastic", QConversionScales="Q in A^-1",
                    LorentzCorrection='1', MinValues=[-15,-15,-15], MaxValues=[15,15,15],
                    SplitInto='2', SplitThreshold='500',MaxRecursionDepth='14',  TopLevelSplitting=1)