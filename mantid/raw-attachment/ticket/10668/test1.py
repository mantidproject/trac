import numpy as np
x = np.concatenate( (np.linspace(-3, 0, 51), np.linspace(0, 3, 76)[1:]) )
xc = ( x[:-1] + x[1:] ) / 2

y = np.exp(-xc**2 * 2)
y[50:] /= 1.5

e = np.ones_like(y)

ws = CreateWorkspace(x,y,e)
