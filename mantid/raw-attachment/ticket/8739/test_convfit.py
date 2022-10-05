from IndirectDataAnalysis import confitSeq


sample =  'osi101944_graphite002_red'
res = FileFinder.getFullPath('osi101913_graphite002_res.nxs')

Load(sample + '.nxs', OutputWorkspace=sample)

func= 'name=LinearBackground,A0=0.001128,A1=0,ties=(A0=0.001128,A1=0.0);(composite=Convolution,FixResolution=true,NumDeriv=true;name=Resolution,FileName="'+res+'",WorkspaceIndex=0;(composite=ProductFunction,NumDeriv=false;name=Lorentzian,Amplitude=2.51312,PeakCentre=1e-05,FWHM=0.001502))'
confitSeq(sample, func, -0.163987, 0.157556, '1L', 'FitL_s',specMin=0,specMax=0,
	       Verbose=False,Plot='None',Save=False)
RenameWorkspace('osi101944_graphite002_conv_1LFitL_0_to_0_0_Workspace', OutputWorkspace='Without')


func= 'name=LinearBackground,A0=0.001128,A1=0,ties=(A0=0.001128,A1=0.0);(composite=Convolution,FixResolution=true,NumDeriv=true;name=Resolution,FileName="'+ res+'",WorkspaceIndex=0;(composite=ProductFunction,NumDeriv=false;name=UserFunction,Formula=(x*11.606/Temp)/(1-exp( -(x*11.606/Temp))),Temp=5;name=Lorentzian,Amplitude=2.51308,PeakCentre=1.1e-05,FWHM=0.001502))'
confitSeq(sample, func, -0.163987, 0.157556, '1L', 'FitL_s',specMin=0,specMax=0,
	       Verbose=False,Plot='None',Save=False)
RenameWorkspace('osi101944_graphite002_conv_1LFitL_0_to_0_0_Workspace', OutputWorkspace='With')