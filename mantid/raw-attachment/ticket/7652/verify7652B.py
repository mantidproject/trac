LoadNexusProcessed(Filename=r'PG3_11485_Fitted.nxs',OutputWorkspace='PG3_11485')
LoadNexusProcessed(Filename=r'braggpeaks.nxs',OutputWorkspace='PG3_11485_Peak')

ProcessBackground(
        InputWorkspace = 'PG3_11485',
        WorkspaceIndex = 0,
        OutputWorkspace= 'PG3_11485_Bkgd',
        Options='RemovePeaks',
        BraggPeakTableWorkspace='PG3_11485_Peak',
        NumberOfFWHM = 2.0,
	UserBackgroundWorkspace = "dummy")

startx = 7730.
endx = 49000.
             
functionstr = "name=%s,n=%d, EndX=%f, StartX=%f" % ("Chebyshev", 12, endx, startx) 
for iborder in xrange(13): 
    functionstr = "%s,A%d=%.5f" % (functionstr, iborder, 0.0) 
Fit( 
        Function        =   functionstr,
        InputWorkspace  =   'PG3_11485_Bkgd',
        Output          =   'PG3_11485_FitBkgd',
        MaxIterations   =   '1000',
        Minimizer       =   'Levenberg-MarquardtMD',
        CreateOutput    =   '1',
        StartX          =   startx,
        EndX            =   endx)



