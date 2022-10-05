# This is a test from a failed unit test requiring the value of Rwp
from math import *

def f(x, a, s, x0): 
    val = exp( -abs(a)*(x-x0)**2/s**2) 
    return val
	
	
vecx = []
vecy = []
vece = []

for i in xrange(10):
    dbl_i = float(i)
    x_i = 0.1*dbl_i
    y_i = 9.9*exp(-(x_i)/0.5)
    e_i = sqrt(y_i)

    vecx.append(x_i)
    vecy.append(y_i)
    vece.append(e_i)
    
# Input
vecx1 = []
vecy1 = []
vece1 = []

for i in xrange(10):
    dbl_i = float(i)
    x_i = 0.1*dbl_i
    y_i = 19.*exp(-(x_i)/0.1)
    e_i = sqrt(y_i)

    vecx1.append(x_i)
    vecy1.append(y_i)
    vece1.append(e_i)
    

CreateWorkspace(OutputWorkspace="Temp", DataX = vecx, DataY = vecy, DataE = vece, NSpec=1)
