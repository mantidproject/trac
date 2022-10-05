import math
# simulate high frequency TF muSR data (therefore not binnable) with small but significant relaxation to be fitted
# arrays to fill
resx=numpy.zeros(200)
resA=numpy.zeros(200)
resAe=numpy.zeros(200)
resS=numpy.zeros(200)
resSe=numpy.zeros(200)
resF=numpy.zeros(200)
resFe=numpy.zeros(200)
resP=numpy.zeros(200)
resPe=numpy.zeros(200)
resChi=numpy.zeros(200)
res0=numpy.zeros(200)
res1=numpy.ones(200)
resIC=numpy.zeros(200)
a0=0.25 # full asymmetry to simulate
freq0=5.0 # MHz
omega=2*math.pi*freq0 # MRad s-1
sig0=0.01 # us-1
tmu=2.197 # muon lifetime
NB=2048 # number of (raw) bins
x12arr=numpy.zeros(2*NB+2)
y12arr=numpy.zeros(2*NB)
e12arr=numpy.zeros(2*NB)
Y1arr=numpy.zeros(NB)
Y2arr=numpy.zeros(NB)
ws=CreateWorkspace(x12arr,y12arr,e12arr,2,OutputWorkspace="Hello")
for x in range(200):
	lam=math.exp((x)/10.0) # counts per bin at t=0 in absence of any signal. Log scale to show detail.
	Xarr=numpy.linspace(0.0,32.768,NB+1,endpoint=True) # "time"
	NomEv=0
	for t in range(NB):
		tt=(Xarr[t]+Xarr[t+1])/2
		a=a0*math.cos(omega*tt)*math.exp(-((sig0*tt)**2))
		lam0=math.exp(-tt/tmu)*lam
		lam1=lam0*(1+a)
		lam2=lam0*(1-a) # counts per bin in forward and backward banks
		Y1arr[t]=numpy.random.poisson(lam1,1)[0] # measured forward counts
		Y2arr[t]=numpy.random.poisson(lam2,1)[0]
		NomEv=NomEv+lam1+lam2
	E1arr=numpy.sqrt(Y1arr) # and their errors by the "standard" formula, Fit() will treat error=0 specially
	E2arr=numpy.sqrt(Y2arr)
	ws.dataX(0)[:]=Xarr
	ws.dataY(0)[:]=Y1arr
	ws.dataE(0)[:]=E1arr
	ws.dataX(1)[:]=Xarr
	ws.dataY(1)[:]=Y2arr
	ws.dataE(1)[:]=E2arr
	AsymmetryCalc(InputWorkspace="Hello",OutputWorkspace="Asym",ForwardSpectra="0",BackwardSpectra="1",alpha=1.0) # re-generated asymmetry
	(stat,chisq,Covar,params,curves)=Fit(Function="name=GausOsc,A=0.24,Sigma=0.03,Frequency=5.0,Phi=0.01",InputWorkspace="Asym",Output="Asym")
	print lam," -> ",params.column(1)[0]," +- ",params.column(2)[0]," chisq=",chisq," st=",stat
	resx[x]=NomEv
	resA[x]=params.column(1)[0]
	resAe[x]=params.column(2)[0]
	resS[x]=params.column(1)[1]
	resSe[x]=params.column(2)[1]
	resF[x]=params.column(1)[2]
	resFe[x]=params.column(2)[2]
	resP[x]=params.column(1)[3]
	resPe[x]=params.column(2)[3]
	resChi[x]=chisq
	DeleteWorkspace("Asym")

	YS1=numpy.sum(Y1arr,dtype=numpy.float) # integral asymmetry of same data for comparison
	YS2=numpy.sum(Y2arr,dtype=numpy.float)
	resIC[x]=YS1+YS2

DeleteWorkspace("Hello")
CreateWorkspace(resx,resA,resAe,1,OutputWorkspace="FittedAsym") # what the fit thought the asymmetry was
CreateWorkspace(resx,resS,resSe,1,OutputWorkspace="FittedSigma") # what the fit thought the sigma was
CreateWorkspace(resx,resF,resFe,1,OutputWorkspace="FittedFreq") # what the fit thought the frequency was
CreateWorkspace(resx,resP,resPe,1,OutputWorkspace="FittedPhase") # what the fit thought the phase was
CreateWorkspace(resx,resChi,res0,1,OutputWorkspace="ChiSquared")

CreateWorkspace(resx,resIC,res0,1,OutputWorkspace="TotalEvents")

p=plotSpectrum("FittedSigma",0,True)
l=p.activeLayer()
l.setAxisScale(Layer.Bottom,100.0,2.0E11,Layer.Log10)
