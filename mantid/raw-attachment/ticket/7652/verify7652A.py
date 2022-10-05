######################################################################
# Test procedure
# 1. Load data
# 2. Select background referring to data points selected by user
# 3. Fit the selected background
# 4. Select background (again) according to the fitted background function
######################################################################
LoadAscii(Filename=r'22946.gda',OutputWorkspace='V22946',Unit='TOF')

ProcessBackground(
        InputWorkspace='V22946',
        OutputWorkspace='V22946_Bkgd01',
        Options='SelectBackgroundPoints',
        BackgroundType='Chebyshev',
        BackgroundOrder='6',
        BackgroundPoints='7449,8413,9217,10709,12183,13110,13317,14539,16103,17683,18700,19717,22912,25000,28900,37444,49000,53000,55000',
        NoiseTolerance='200',
        UserBackgroundWorkspace='FilterRef01',
        SelectionMode = 'FitGivenDataPoints'
        )

startx = 7360.
endx = 55375.
            
functionstr = "name=%s,n=%d, EndX=%f, StartX=%f" % ("Chebyshev", 12, endx, startx) 
for iborder in xrange(13): 
    functionstr = "%s,A%d=%.5f" % (functionstr, iborder, 0.0) 
Fit( 
        Function        =   functionstr,
        InputWorkspace  =   'V22946_Bkgd01',
        Output          =   'V22946_Bkgd01',
        MaxIterations   =   '1000',
        Minimizer       =   'Levenberg-MarquardtMD',
        CreateOutput    =   '1',
        StartX          =   startx,
        EndX            =   endx)


ProcessBackground(
        InputWorkspace='V22946',
        OutputWorkspace='V22946_Bkgd02',
        Options='SelectBackgroundPoints',
        LowerBound = startx,
        UpperBound = endx,
        BackgroundType='Chebyshev',
        SelectionMode = 'UserFunction',
        BackgroundTableWorkspace = 'V22946_Bkgd01_Parameters',
        NoiseTolerance='100',
        UserBackgroundWorkspace='FilterRef02')

functionstr = "name=%s,n=%d, EndX=%f, StartX=%f" % ("Chebyshev", 12, endx, startx) 
for iborder in xrange(13): 
    functionstr = "%s,A%d=%.5f" % (functionstr, iborder, 0.0) 
Fit( 
        Function        =   functionstr,
        InputWorkspace  =   'V22946_Bkgd02',
        Output          =   'V22946_Bkgd02',
        MaxIterations   =   '1000',
        Minimizer       =   'Levenberg-MarquardtMD',
        CreateOutput    =   '1',
        StartX          =   startx,
        EndX            =   endx)
