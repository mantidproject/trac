from mantid.simpleapi import * 
#prepare data to the input of CalculateTransmission
ws = LoadRaw("LOQ48097.raw", SpectrumMin=1, SpectrumMax=2);
ws = ConvertUnits(ws, Target="Wavelength")
m_dirWS = Rebin(ws, "6, 0.01, 7.5",OutputWorkspace="CalculateTransmissionTest_direct")
m_transWS = Rebin(ws, "7.5, 0.01, 9",OutputWorkspace="CalculateTransmissionTest_trans")
m_dirWS.setX(0, m_transWS.dataX(0))
m_dirWS.setX(1, m_transWS.dataX(0))

outlog = CalculateTransmission(m_transWS, m_dirWS, 1, 2,FitMethod='Log',OutputUnfittedData=True)
out2 = CalculateTransmission(m_transWS, m_dirWS, 1, 2,FitMethod='Polynomial', PolynomialOrder=2,OutputUnfittedData=True)
outlinear = CalculateTransmission(m_transWS, m_dirWS, 1, 2,FitMethod='Linear',OutputUnfittedData=True)


unfitted = mtd['outlog_unfitted']
unf_log = Logarithm(unfitted, Natural=True)
func_name ='name=LinearBackground'
func_name = "name=Polynomial,n=2"
Fit(Function=func_name, InputWorkspace=unf_log, CreateOutput=True, Output='unf_log_fit')
unf_log_fit = ExtractSingleSpectrum('unf_log_fit_Workspace',1)
fitted = Exponential(unf_log_fit)

fitted_err = CreateWorkspace(range(len(fitted.dataE(0))),fitted.dataE(0))
out2 = out2[0]
calc_err = CreateWorkspace(range(len(fitted.dataE(0))),out2.dataE(0))


# if you plot outlog, out2 and outlinear they should be similar. 

# fitted and out2 should be identical (the error will be slightly different due to an error to be dealt in #9011
