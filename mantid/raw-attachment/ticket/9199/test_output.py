import numpy as np

def noise(n):
	return ( np.random.random(n)  - 0.5 ) / 10

ws = CreateWorkspace('-10,10,-10,10,-10,10','0,0,0,0,0,0',NSpec=3)
ws = Rebin('ws','-10,0.01,10')
n = ws.blocksize()
x = ws.readX(0)
ws.setY(0, np.exp( -(x+1.0)**2/0.99 ) * 1.1 + noise(n) )
ws.setY(1, np.exp( -(x)**2 ) + noise(n) )
ws.setY(2, np.exp( -(x-1.0)**2/1.01 ) * 0.9 + noise(n) )

fun = 'name=Gaussian,$domains=i,Height=1,Sigma=1,PeakCentre=0'
muli_domain = 'composite=MultiDomainFunction;(%s);(%s);(%s);ties=(f2.Sigma=f1.Sigma=f0.Sigma)' % (fun,fun,fun)

kwargs = {\
		'WorkspaceIndex': 0,
		'InputWorkspace_1':'ws',
		'WorkspaceIndex_1': 1,
		'InputWorkspace_2':'ws',
		'WorkspaceIndex_2': 2,
		}

Fit(muli_domain,'ws',Output='out',**kwargs)
