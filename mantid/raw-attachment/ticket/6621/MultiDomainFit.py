Load(r'C:\Users\hqs74821\Work\mantid\Test\AutoTestData\MUSR00015189.nxs',OutputWorkspace='musr')
inputWS = 'musr_1'
nHist = 3#mtd[inputWS].getNumberHistograms()
outNm = 'output' #getWSprefix(inputWS) + 'fury'
f1 = """(
    composite=CompositeFunction,$domains=i;
    name=LinearBackground,A0=0,A1=0,ties=(A1=0);
    name=UserFunction,Formula=Intensity*exp(-(x/Tau)^Beta),Intensity=1.0,Tau=0.1,Beta=1;ties=(f1.Intensity=1-f0.A0)
);
"""#.replace('$WORKSPACE$',inputWS)
func= 'composite=MultiDomainFunction,NumDeriv=1;'
ties='ties=('
kwargs = {}
for i in range(0,nHist):
    func+=f1
    if i > 0:
        ties += 'f' + str(i) + '.f1.Beta=f0.f1.Beta'
        if i < nHist-1:
            ties += ','
	kwargs['InputWorkspace_' + str(i)] = inputWS
	kwargs['WorkspaceIndex_' + str(i)] = i
	
ties+=')'
func += ties
logger.notice(func)
logger.notice(str(kwargs))
Fit(Function=func,InputWorkspace=inputWS,WorkspaceIndex=0,Output=outNm,Minimizer='Levenberg-MarquardtMD,Debug=1',**kwargs)
