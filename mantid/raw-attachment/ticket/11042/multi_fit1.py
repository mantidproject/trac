d0 = Load('d0.nxs')
d1 = Load('d1.nxs')

ft = 'name=Gaussian,PeakCentre=0,Height=1,Sigma=0.5,$domains=%s'

# swap 0 <--> 1
f0 = ft % 0
f1 = ft % 1

# swap f0 <--> f1
ties = ';ties = (f0.Height=f1.Height)'

func = 'composite=MultiDomainFunction,NumDeriv=1;%s;%s %s' % (f0,f1,ties)

Fit(func,InputWorkspace='d0',InputWorkspace_1='d1', Output='out')
