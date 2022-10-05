# Need to have the systemtest directory checkout and in search path
Load(Filename='TOPAZ_3132_event.nxs', OutputWorkspace='TOPAZ_3132_event')
ConvertToMD(InputWorkspace='TOPAZ_3132_event', OutputWorkspace='TOPAZ_3132_MD', QDimensions='Q3D', dEAnalysisMode='Elastic', LorentzCorrection='1', MinValues='-25,-25,-25', MaxValues='25,25,25', SplitInto='2,2,2', SplitThreshold='50', MaxRecursionDepth='13', MinRecursionDepth='7')
FindPeaksMD(InputWorkspace='TOPAZ_3132_MD', PeakDistanceThreshold='0.5', MaxPeaks='150', OutputWorkspace='TOPAZ_3132_peaks')
FindUBUsingFFT(PeaksWorkspace='TOPAZ_3132_peaks', MinD='3', MaxD='15', Tolerance='0.12')
IndexPeaks(PeaksWorkspace='TOPAZ_3132_peaks', Tolerance='0.12')
