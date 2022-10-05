#Introduce the proper path to the foler where the data files are
data_path= 'C:/Users/epr30176/Downloads/'

ws_data = Load(Filename=data_path+'irs26176_graphite002_red.nxs')
ws_res = Load(Filename=data_path+'irs26173_graphite002_res.nxs')

function_str = 'composite=Convolution,FixResolution=tue,NumDeriv=false;name=Resolution,Workspace=ws_res,WorkspaceIndex=0;(composite=CompositeFunction,NumDeriv=true;name=Lorentzian,Amplitude=1,PeakCentre=0.01,FWHM=0.5;name=Lorentzian,Amplitude=1,PeakCentre=0.01,FWHM=0.5)'
minimizer_str = "FABADA,Chain Lengh=1000000,Steps between values=10,Convergence Criteria=0.01,PDF='pdf',Chains='chain',Converged chain='conv',Cost Function Table=CostFunction,Parameter Erros =Errors"

Fit(Function = function_str,InputWorkspace=ws_data,WorkspaceIndex=3,StartX=-0.25,EndX=0.25,CreateOutput=True,Output = 'result',OutputCompositeMembers=True,MaxIterations=2000000, Minimizer=minimizer_str)   

'''
Properties of the minimizer:

Chain Lengh: number of steps to do (once it is converged)
Steps between values: it is considered just one value for each number of steps depeding on this parameter (for avoiding correlation with itselves)  
Convergence Criteria: maximum variation (in) % of the cost function which is cosidered as convergence

Output generated:

chain: each line of the ws is the value of a parameter in each step. The last line is for the cost function value

conv: the same structure as before, but cotaining just the converged part of the chain and only one value each "steps between values" steps.

pdf: each line of the ws is the probaility distribution function (histogram) of a parameter. The last line is for the cost function pdf

Errors: table with the values of the parameters and its errors

CostFuction: table wih the values of the minimum cost function, the most probable and the coresponding reduced ones. 
"""