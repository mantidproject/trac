import numpy as np

m = 200
n = 64
X = np.ones(m*n)

ws = CreateWorkspace(X,X,X,n,'MomentumTransfer')

for i in range(n):
	x0 = -10 + i * 0.1
	x1 = x0 + 20
	x = np.linspace(x0,x1,m)
	y = np.exp(-x**2)
	ws.setX(i,x)
	ws.setY(i,y)

LoadInstrument(ws,InstrumentName='MUSR')
