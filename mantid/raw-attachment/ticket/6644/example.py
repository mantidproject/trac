LoadSassena(Filename='/tmp/example.h5',OutputWorkspace='example')
SassenaFFT(InputWorkspace='example',FFTonlyRealPart=1)
CloneWorkspace(InputWorkspace='example_sqw',OutputWorkspace='cloned')
SassenaFFT(InputWorkspace='example',FFTonlyRealPart=0)
