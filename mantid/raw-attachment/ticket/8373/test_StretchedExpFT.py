ws = LoadAscii(Filename='/tmp/stretchedExpFT.dat', Separator='Space', OutputWorkspace='data')
fitstring = 'name=StretchedExpFT,height=0.1,tau=100.0,beta=1.0'  # The initial guess must be reasonably close
Fit(Function=fitstring, InputWorkspace='data', CreateOutput=1)
