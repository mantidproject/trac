LoadSassena(Filename='/tmp/example.h5',OutputWorkspace='example')
SassenaFFT(InputWorkspace='example',FFTonlyRealPart=1)
CloneWorkspace(InputWorkspace='example_sqw',OutputWorkspace='transformed_of_real_part')
DeleteWorkspace('example_sqw')
SassenaFFT(InputWorkspace='example',FFTonlyRealPart=0)
CloneWorkspace(InputWorkspace='example_sqw',OutputWorkspace='transformed_of_real_plus_imaginary')