LoadGSS(Filename=r'PG3_4866.gsa',OutputWorkspace='PG3_4866',UseBankIDasSpectrumNumber='1')
FitPeak(InputWorkspace='PG3_4866',OutputWorkspace='peak5_model',ParameterTableWorkspace='peak5_parameters',PeakFunctionType='Gaussian (Height, PeakCentre, Sigma)',
	PeakParameterValues='100,11190,20',BackgroundType='Quadratic',BackgroundParameterNames='A0,A1,A2',BackgroundParameterValues='0,0,0',FitWindow='11000,11400',
	PeakRange='11800,11300',CostFunction='Rwp')
