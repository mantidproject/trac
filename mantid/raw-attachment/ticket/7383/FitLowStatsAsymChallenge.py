import math
# arrays to fill
resx=numpy.zeros(200)
resy=numpy.zeros(200)
rese=numpy.zeros(200)
resChi=numpy.zeros(200)
res0=numpy.zeros(200)
res1=numpy.ones(200)
resNZ=numpy.zeros(200)
resIC=numpy.zeros(200)
resICE=numpy.zeros(200)
a=0.25 # asymmetry to simulate
NB=1000 # number of (raw) bins
x12arr=numpy.zeros(2*NB)
y12arr=numpy.zeros(2*NB)
e12arr=numpy.zeros(2*NB)
ws=CreateWorkspace(x12arr,y12arr,e12arr,2,OutputWorkspace="Hello")
for x in range(200):
	lam=math.exp((x-75.0)/10.0) # counts per bin, in absence of any signal. Log scale to show detail.
	lam1=lam*(1+a)
	lam2=lam*(1-a) # counts per bin in forward and backward banks
	Xarr=range(NB) # "time"
	Y1arr=numpy.random.poisson(lam1,NB) # measured forward counts
	E1arr=numpy.sqrt(Y1arr) # and their errors by the "standard" formula, Fit() will treat error=0 specially
	Y2arr=numpy.random.poisson(lam2,NB)
	E2arr=numpy.sqrt(Y2arr)
	ws.dataX(0)[:]=Xarr
	ws.dataY(0)[:]=Y1arr
	ws.dataE(0)[:]=E1arr
	ws.dataX(1)[:]=Xarr
	ws.dataY(1)[:]=Y2arr
	ws.dataE(1)[:]=E2arr
	AsymmetryCalc(InputWorkspace="Hello",OutputWorkspace="Asym",ForwardSpectra="0",BackwardSpectra="1",alpha=1.0) # re-generated asymmetry
	(stat,chisq,Covar,params,curves)=Fit(Function="name=FlatBackground,A0=0.1",InputWorkspace="Asym",Output="Asym")
	print lam," -> ",params.column(1)[0]," +- ",params.column(2)[0]," chisq=",chisq," st=",stat
	resx[x]=lam
	resy[x]=params.column(1)[0]
	rese[x]=params.column(2)[0]
	resNZ[x]=(len(Y1arr)-numpy.count_nonzero(Y1arr)+len(Y2arr)-numpy.count_nonzero(Y2arr))/(len(Y1arr)+len(Y2arr)+0.0)
	resChi[x]=chisq
	DeleteWorkspace("Asym")

	YS1=numpy.sum(Y1arr,dtype=numpy.float) # integral asymmetry of same data for comparison
	YS2=numpy.sum(Y2arr,dtype=numpy.float)
	if(YS1+YS2>0):
		resIC[x]=(YS1-YS2)/(YS1+YS2)
		resICE[x]=2.0*math.sqrt(YS1*YS2)*(YS1+YS2)**(-1.5)
	else:
		resIC[x]=float('NaN')
		resICE[x]=float('Inf') # no counts, asymmetry completely uncertain!

DeleteWorkspace("Hello")
CreateWorkspace(resx,resy,rese,1,OutputWorkspace="Summary") # what the fit thought the asymmetry was
CreateWorkspace(resx,resNZ,res0,1,OutputWorkspace="FractionOfZeros")
DiffOverErr=(resy-a)/rese
CreateWorkspace(resx,DiffOverErr,res1,1,OutputWorkspace="NormalisedDifference") # if outside +-1 then systematic errors are significant
CreateWorkspace(resx,resChi,res0,1,OutputWorkspace="ChiSquared")

CreateWorkspace(resx,resIC,resICE,1,OutputWorkspace="IntegralCounted")

p=plotSpectrum("Summary",0,True)
l=p.activeLayer()
l.setAxisScale(Layer.Bottom,0.001,1000000.0,Layer.Log10)

p2=plotSpectrum("NormalisedDifference",0,True)
l2=p2.activeLayer()
l2.setAxisScale(Layer.Bottom,0.001,1000000.0,Layer.Log10)
