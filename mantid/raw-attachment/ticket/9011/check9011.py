import ISISCommandInterface as ici
import math
MASKFILE = FileFinder.getFullPath('MaskSANS2DReductionGUI.txt')
    
ici.SANS2D()
ici.MaskFile(MASKFILE)
ici.TransFit('LOG')
ici.AssignSample('22048')
ici.TransmissionSample('22041','22024')
reduced = ici.WavRangeReduction()

# apply ln
log_natural = Logarithm('22041_trans_sample_1.5_12.5_unfitted', Natural=True)
# fit
Fit(Function='name=LinearBackground',InputWorkspace=log_natural,Minimizer='Levenberg-MarquardtMD',CreateOutput='1',Output='linear_background',StartX='1.5',EndX='12.5')
fitted_log_values = ExtractSingleSpectrum('linear_background_Workspace', 1)
# apply exp()
fit_lognatural_values = Exponential(fitted_log_values)


# apply log10
log_10 = Logarithm('22041_trans_sample_1.5_12.5_unfitted', Natural=False)
Fit(Function='name=LinearBackground',InputWorkspace=log_10,Minimizer='Levenberg-MarquardtMD',CreateOutput='1',Output='linear_background',StartX='1.5',EndX='12.5')
fitted_log10_values = ExtractSingleSpectrum('linear_background_Workspace', 1)
# apply pow(10) => exp(ln10*x)
fitted_log_values = math.log(10) * fitted_log10_values
fit_log_values = Exponential(fitted_log_values)



