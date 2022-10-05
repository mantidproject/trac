'''This is a fit to data.nxs using the convolution of a resolution and a DiffRotDiscreteCircle function.
The data and resolution correspond to an experiment of Octa-Methyl Silsesquioxane molecules
carried out at 200K

data.nxs is such that the optimized parameters should be:

   Intensity = 0.745,  Radius = 0.876(Angstroms),  Decay = 763.6(pico-seconds)

In DiffRotDiscreteCircle, "N" and "Q " are attributes, not fitting parameters.
Data corresponds to Q=1.9. This is a fit to methyl rotations, thus N-3 was selected

I chose starting parameters in "fitstring" reasonable far apart from
the optimal values. Feel free to change this initial guess.

The units for this example are:
  [Intensity] = arbitray units
  [Radius] = Angstroms
  [Decay] = pico-seconds
  [X-values in data.nxs] = micro-eV
  
'''
data = LoadNexus(Filename='/tmp/data.nxs')
elastic = LoadNexus(Filename='/tmp/resolution.nxs')
fitstring='(composite=Convolution,FixResolution=true,NumDeriv=true;name=TabulatedFunction,FileName="",Workspace=resolution,Scaling=1;(name=DiffRotDiscreteCircle,N=3,NumDeriv=true,Q=1.9,Intensity=1,Radius=1,Decay=10));name=LinearBackground,A0=0.001,A1=0.0001'
Fit(Function=fitstring, InputWorkspace='data', CreateOutput=1)
