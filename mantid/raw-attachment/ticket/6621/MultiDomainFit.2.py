# load some data
Load(r'MUSR00015189.nxs',OutputWorkspace='musr')
# use first workspace in the group
inputWS = 'musr_1'
# rebin to remove negative values causing problems
musr_1 = Rebin('musr_1','0.5,0.1,30')
# 
musr_2 = Rebin('musr_2','0.5,0.1,30')
musr_2 *= 2
musr_3 = Rebin('musr_2','0.5,0.1,30')
musr_3 *= 1.5
workspaces = ['musr_1','musr_2','musr_3']
# we will fit 3 spectra simultaneously: one from each workspace
nHist = 3
outNm = 'output'
# template for function to fit each spectrum
# the $ sign means that the attribute is to be passed to the parent composite function along with this function's index
f1 = """(
    composite=CompositeFunction,$domains=i;
    name=LinearBackground,A0=0,A1=0,ties=(A1=0);
    name=UserFunction,Formula=Intensity*exp(-(x/Tau)^Beta),Intensity=1000.0,Tau=2,Beta=1
);
"""
# top-level function is MultiDomainFunction
# ensure that numerical derivatives are used
func= 'composite=MultiDomainFunction,NumDeriv=1;'
# to tie all Betas together
ties='ties=('
# collect properties to specify additional spectra
kwargs = {}
for i in range(0,nHist):
    # for each spectrum add its function
    func+=f1
    if i > 0:
        # tie f1.f1.Beta = f2.f1.Beta = f0.f1.Beta
        ties += 'f' + str(i) + '.f1.Beta=f0.f1.Beta'
        if i < nHist-1:
            ties += ','
        # workspace name and spectrum index for the last two spectra
	kwargs['InputWorkspace_' + str(i)] = workspaces[i]
	kwargs['WorkspaceIndex_' + str(i)] = i
	
ties+=')'
# ties applied at MultiDomainFunction's level
func += ties
logger.notice(func)
logger.notice(str(kwargs))
# do the fit
Fit(Function=func,InputWorkspace=workspaces[0],WorkspaceIndex=0,Output=outNm,Minimizer='Levenberg-MarquardtMD,Debug=1',**kwargs)
