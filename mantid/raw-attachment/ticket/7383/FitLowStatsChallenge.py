import math
# arrays to fill
resx=numpy.zeros(200)
resy=numpy.zeros(200)
rese=numpy.zeros(200)
resChi=numpy.zeros(200)
res0=numpy.zeros(200)
resNZ=numpy.zeros(200)
NB=10000 # number of bins
x12arr=numpy.zeros(NB)
y12arr=numpy.zeros(NB)
e12arr=numpy.zeros(NB)
ws=CreateWorkspace(x12arr,y12arr,e12arr,1,OutputWorkspace="Hello")
for x in range(200):
	lam=math.exp((x-75.0)/10.0) # expected rate (log scale to show detail)
	Xarr=range(NB) # "time" bins
	Yarr=numpy.random.poisson(lam,NB) # actual counts
	Earr=numpy.sqrt(Yarr) # and the errors
	ws.dataX(0)[:]=Xarr
	ws.dataY(0)[:]=Yarr
	ws.dataE(0)[:]=Earr
	(stat,chisq,Covar,params,curves)=Fit(Function="name=FlatBackground,A0=1.0",InputWorkspace="Hello",Output="Hello")
	print lam," -> ",params.column(1)[0]," +- ",params.column(2)[0]," chisq=",chisq," st=",stat
	resx[x]=lam
	resy[x]=params.column(1)[0]
	rese[x]=params.column(2)[0]
	resNZ[x]=(len(Yarr)-numpy.count_nonzero(Yarr))/(len(Yarr)+0.0)
	resChi[x]=chisq

DeleteWorkspace("Hello")
CreateWorkspace(resx,resy,rese,1,OutputWorkspace="Summary") # what the fit thought the count rate was
CreateWorkspace(resx,resx,res0,1,OutputWorkspace="Ideal") # the intended count rate to plot alongside
CreateWorkspace(resx,resNZ,res0,1,OutputWorkspace="FractionOfZeros")
CreateWorkspace(resx,resChi,res0,1,OutputWorkspace="ChiSquared")

Minus(LHSWorkspace='Summary',RHSWorkspace='Ideal',OutputWorkspace='FitDifference')
Divide(LHSWorkspace='Summary',RHSWorkspace='Ideal',OutputWorkspace='FitRatio')

p=plotSpectrum("FitDifference",0,True)
l=p.activeLayer()
l.setAxisScale(Layer.Bottom,0.001,1000000.0,Layer.Log10)

p2=plotSpectrum("FitRatio",0,True)
l2=p2.activeLayer()
l2.setAxisScale(Layer.Bottom,0.001,1000000.0,Layer.Log10)
