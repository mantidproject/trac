fun = '(composite=Convolution,FixResolution=true,NumDeriv=true;name=Resolution,Workspace=resolution3,WorkspaceIndex=0;name=Gaussian,Height=0.5,PeakCentre=0,Sigma=1.5)'
data3 = Load('data3.nxs')
resolution3 = Load('resolution3.nxs')

PlotPeakByLogValue('data3,i0;data3,i1;data3,i2',fun,OutputWorkspace='result',PassWSIndexToFunction=True,FitType='Sequential')
