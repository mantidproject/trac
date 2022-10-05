# Ticket 8624, branch feature/8624_improve_time_sampling_stExFT
# (note: hbar = 0.658211626 meV * THz )
# Fitting parameters to test:
#
# The lorentzian structure factor has HWMW = 0.013meV. After the fitting, the
# tau parameter should be: tau = hbar / HWMW = 50.63166352pico-seconds. It's OK if the result
# is off by a few percent
#
# The Gaussian structure factor has sigma = 0.047meV. After the fitting, the
# tau parameter should be: tau = sqrt(2) * hbar / HWMW = 19.805357618pico-seconds. It's OK if the result
# is off by a few percent
#
workdir = '/tmp'

LoadAscii( Filename = '{0}/lorentzian1.dat'.format(workdir), OutputWorkspace = 'lorentzian' )
fit_string = 'name=StretchedExpFT,height=0.1,tau=10.0,beta=1.0,ties=(beta=1.0)'
Fit( fit_string, InputWorkspace = 'lorentzian', CreateOutput = 1 ) #check workspace lorentzian_Parameters

LoadAscii( Filename = '{0}/gaussian1.dat'.format(workdir), OutputWorkspace = 'gaussian' )
fit_string = 'name=StretchedExpFT,height=0.1,tau=10.0,beta=2.0,ties=(beta=2.0)'
Fit( fit_string, InputWorkspace = 'gaussian', CreateOutput = 1 ) #check workspace gaussian_Parameters
