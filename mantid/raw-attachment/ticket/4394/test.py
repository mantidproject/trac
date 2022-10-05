'''This is a fit to data.nxs using the convolution of a resolution and a DiffRotDiscreteCircle function.
The data and resolution correspond to an experiment of Octa-Methyl Silsesquioxane molecules
carried out at 200K

data.nxs is such that the optimized parameters should be:
       Intensity = 0.74,  Radius = 2.25,  Diffusion = 0.024
After the fit, check workspace data_Parameters for f1.f1 parameters

The units for this example are:
  [Intensity] = arbitray units
  [Radius] = Angstroms
  [Diffusion] = Anstroms^2 / pico-seconds
  [X-values in data.nxs] = mili-eV
'''

workdir = '/tmp'
LoadNexus(Filename='{0}/data.nxs'.format( workdir), OutputWorkspace='data' )
LoadNexus(Filename='{0}/resolution.nxs'.format( workdir), OutputWorkspace='resolution' )

#The fitstring defines the model:  A * Elastic + B*Convolution( Elastic, DiffSphere) + LinearBackground
fitstring='name=TabulatedFunction,Workspace=resolution,WorkspaceIndex=0,Scaling=0.02,constraints=(0.0001<Scaling);(composite=Convolution,FixResolution=true,NumDeriv=true;name=TabulatedFunction,Workspace=resolution,WorkspaceIndex=0,Scaling=1;(name=DiffSphere,NumDeriv=true,Q=1.0,Intensity=0.2,Radius=4.0,Diffusion=0.05));name=LinearBackground,A0=0.0,A1=-0.0'

Fit(Function=fitstring, InputWorkspace='data', StartX=-0.1, EndX=0.1, CreateOutput=1)
