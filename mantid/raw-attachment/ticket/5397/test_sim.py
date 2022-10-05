"""A test script to compare a simulation of MERLIN convolved with a foreground model
"""
from mantid.simpleapi import *
from mantid.kernel import V3D
import os

def create_cuboid_xml(xlength,ylength,zlength):
    xml = """<cuboid id="sample0">
<left-front-bottom-point x="%(xpt)f" y="-%(ypt)f" z="-%(zpt)f"  />
<left-front-top-point  x="%(xpt)f" y="-%(ypt)f" z="%(zpt)f"  />
<left-back-bottom-point  x="-%(xpt)f" y="-%(ypt)f" z="-%(zpt)f"  />
<right-front-bottom-point  x="%(xpt)f" y="%(ypt)f" z="-%(zpt)f"  />
</cuboid>
<algebra val="sample0" />
"""
    return xml % {"xpt": xlength/2.0,"ypt":ylength/2.0,"zpt":zlength/2.0}


data_dir = '/home/dmn58364/mantidproject/test-scripts/inelastic/tobyfit/mantid'

ei = 300.
bins = [-30,3,279]
temperature = 6. 
chopper_speed = 600.

# Oriented lattice & goniometer
alatt = 5.57
blatt = 5.51
clatt = 12.298
uvec = [9.700000e-03,9.800000e-03,9.996000e-01]
vvec = [9.992000e-01,-3.460000e-02,-4.580000e-02]
psi = 0.0
omega = 0.0
alpha = 0.0
beta = 0.0
gamma = 0.0

# sample dimensions
sx = 0.05
sy = 0.025
sz = 0.04

# Crystal mosaic
eta_sig = 4.0

## 
## A fake data set for simulation purposes.
##
fake_data = CreateSimulationWorkspace(Instrument='MERLIN',BinParams=bins,UnitX='DeltaE',
                                      DetectorTableFilename=os.path.join(data_dir,'MER06398.raw'))

nhist = fake_data.getNumberHistograms()
nbins = fake_data.blocksize()
print 'nbins*nhist',nhist*nbins

##
## Required log entries, can be taken from real ones by placing an instrument parameter of the same
## name pointing to the log name
##
AddSampleLog(Workspace=fake_data, LogName='Ei',LogText=str(ei), LogType="Number")
AddSampleLog(Workspace=fake_data, LogName='temperature_log',LogText=str(temperature), LogType="Number")
AddSampleLog(Workspace=fake_data, LogName='chopper_speed_log',LogText=str(chopper_speed), LogType="Number")
AddSampleLog(Workspace=fake_data, LogName='eta_sigma',LogText=str(eta_sig), LogType="Number")


##
## OrientedLattice & Goniometer to define rotations
##
SetUB(Workspace=fake_data,a=alatt,b=blatt,c=clatt,u=uvec,v=vvec)
# AddSampleLog(Workspace=fake_data,LogName='psi',LogText=str(psi),LogType='Number')
# AddSampleLog(Workspace=fake_data,LogName='omega',LogText=str(omega),LogType='Number')
# AddSampleLog(Workspace=fake_data,LogName='alpha',LogText=str(alpha),LogType='Number')
# AddSampleLog(Workspace=fake_data,LogName='beta',LogText=str(beta),LogType='Number')
# AddSampleLog(Workspace=fake_data,LogName='gamma',LogText=str(gamma),LogType='Number')
# SetGoniometer(Workspace=fake_data,Axis0="psi,0,1,0,1",Axis1="omega,0,1,0,1",
#               Axis2="gamma,0,1,0,1",Axis3="beta,1,0,0,1",Axis4="alpha,0,0,1,1")

##
## Sample shape
##
CreateSampleShape(InputWorkspace=fake_data, ShapeXML=create_cuboid_xml(sx,sy,sz))

##
## Chopper & Moderator models. 
##
CreateModeratorModel(Workspace=fake_data,ModelType='IkedaCarpenterModerator',
                     Parameters="TiltAngle=32,TauF=2.7,TauS=0,R=0")
CreateChopperModel(Workspace=fake_data,ModelType='FermiChopperModel',
                   Parameters="AngularVelocity=chopper_speed_log,ChopperRadius=0.049,SlitThickness=0.0023,SlitRadius=1.3,Ei=Ei")

##
## Create the MD workspace 
##
simulws = ConvertToMD(InputWorkspace=fake_data, QDimensions="Q3D", SplitInto=[3], SplitThreshold=100,
                      MinValues="-15,-15,-15,-30", MaxValues="25,25,25,279")

##
## Run the simulation
##
resol_model = "TobyFitResolutionModel"
xsec_model = "Strontium122"
parameters = "Seff=0.7,J1a=38.7,J1b=-5.0,J2=27.3,SJc=10.0,GammaSlope=0.08,MultEps=0,TwinType=0,MCLoopMax=1000"
simulated_ws = SimulateResolutionConvolvedModel(InputWorkspace=simulws,
                                                ResolutionFunction=resol_model,
                                                ForegroundModel=xsec_model,
                                                Parameters=parameters)

#simulated_file = 'mer300meV_psi0_sim_mantid_1.nxs'
#SaveMD(InputWorkspace=simulated_ws,Filename=os.path.join(data_dir,simulated_file))
