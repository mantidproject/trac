try:
    from mantidplottests import screenshot
except ImportError:
    def screenshot(*args,**kwargs):
        pass

from mantid.simpleapi import *
import math
import sys

#=================== helper functions ===============================

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
 
def plot_slice(in_ws, out_ws):
	BinMD(InputWorkspace=in_ws, OutputWorkspace=out_ws,
		AlignedDim0='[H,0,0], -12.000000, 9.000000, 100',
		AlignedDim1='[0,K,0], -6.000000, 7.000000, 100',
		AlignedDim2='[0,0,L], 0.000000, 6.000000, 1',
		AlignedDim3='DeltaE, 100.000000, 150.000000, 1')
	plotSlice(out_ws,colormax=180,normalization=0)

#============================================================

ei = 300.
bins = [-30,3,279]
temperature = 6.
chopper_speed = 600.
 
# Oriented lattice & goniometer.
alatt = 5.57
blatt = 5.51
clatt = 12.298
uvec = [9.700000e-03,9.800000e-03,9.996000e-01]
vvec = [9.992000e-01,-3.460000e-02,-4.580000e-02]

omega = 0.0
alpha = 0.0
beta = 0.0
gamma = 0.0
 
# sample dimensions
sx = 0.05 # Perp
sy = 0.025 # Up direction
sz = 0.04 # Beam direction
 
# Crystal mosaic
eta_sig = 4
 
data_dir = '/data/Software/VATES_testing/Sr122_tests/'

 
#Use Iliad processed workspace for simulation
# Workspaces from Iliad have had their source component moved to redefine the location of t0 to the first monitor
# It needs to be put back in the proper place here
base_moderator = mtd['w1'].getInstrument().getBaseInstrument().getSource()
mod_pos = base_moderator.getPos()
MoveInstrumentComponent('w1',ComponentName=base_moderator.getName(),X=mod_pos.getX(), 
                                             Y=mod_pos.getY(),Z=mod_pos.getZ(),RelativePosition=False)


##
## Required log entries, can be taken from real ones by placing an instrument parameter of the same
## name pointing to the log name
##
AddSampleLog(Workspace='w1', LogName='Ei',LogText=str(ei), LogType="Number")
AddSampleLog(Workspace='w1', LogName='temperature_log',LogText=str(temperature), LogType="Number")
AddSampleLog(Workspace='w1', LogName='chopper_speed_log',LogText=str(chopper_speed), LogType="Number")
AddSampleLog(Workspace='w1', LogName='eta_sigma',LogText=str(eta_sig), LogType="Number")
 
##
## Sample shape
##
CreateSampleShape(InputWorkspace='w1', ShapeXML=create_cuboid_xml(sx,sy,sz))
 
##
## Chopper & Moderator models. 
##
CreateModeratorModel(Workspace='w1',ModelType='IkedaCarpenterModerator',
                     Parameters="TiltAngle=32,TauF=2.7,TauS=0,R=0")
CreateChopperModel(Workspace='w1',ModelType='FermiChopperModel',
                   Parameters="AngularVelocity=chopper_speed_log,ChopperRadius=0.049,SlitThickness=0.0023,SlitRadius=1.3,Ei=Ei,JitterSigma=0.0")
 
##
## UB matrix
##
SetUB(Workspace='w1',a=alatt,b=blatt,c=clatt,u=uvec,v=vvec)
 
##
## Sample rotation. Simulate 1 run at zero degrees psi
##

psi = 0.0
AddSampleLog(Workspace='w1',LogName='psi',LogText=str(psi),LogType='Number')
SetGoniometer(Workspace='w1',Axis0="psi,0,1,0,1")

# Create the MD workspace
qscale = 'Q in A^-1'
sr122_md = ConvertToMD(InputWorkspace='w1', QDimensions="Q3D", QConversionScales=qscale,SplitInto=[3], SplitThreshold=100,
		      MinValues="-15,-15,-15,-30", MaxValues="25,25,25,279",OverwriteExisting=True)
 
 #Modified version of the simulation, with greater control of which contributions to the resolution model we have:
resol_model = "TobyFitResolutionModel"
fg_model = "Strontium122"
		 						  
						  
fg_parameters = "Seff=0.7,J1a=38.7,J1b=-5,J2=27.3,SJc=10,GammaSlope=0.08,MultEps=0,TwinType=1,FormFactorIon=0"
xsec_model = "Strontium122"
# Just forground model, no resolution convolution. Should reproduce exactly what Tobyfit does...
# Sequentially work through the invidiual contributions to the resolution:
res_parameters = "MCLoopMin=10,MCLoopMax=10,MCType=1,ForegroundOnly=1" 
parameters = res_parameters +  "," + fg_parameters

# Sequentially work through the invidiual contributions to the resolution:

## Moderator ##
res_parameters = "MCLoopMin=10,MCLoopMax=10,MCType=1,Moderator=1,Chopper=0,ChopperJitter=0,Aperture=0,SampleVolume=0,DetectorDepth=0,DetectorArea=0,DetectionTime=0,CrystalMosaic=0" 
parameters = res_parameters +  "," + fg_parameters
simulated_mod= SimulateResolutionConvolvedModel(InputWorkspace="sr122_md",
                                            ResolutionFunction=resol_model,
                                            ForegroundModel=xsec_model,Parameters=parameters)
BinMD(InputWorkspace="simulated_mod", OutputWorkspace="simulated_mod_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')
mt_mod_table=QueryMDWorkspace('simulated_mod_cut')
mt_mod_sim=ConvertTableToMatrixWorkspace('mt_mod_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')


## Sample Volume ##
res_parameters = "MCLoopMin=10,MCLoopMax=10,MCType=1,Moderator=0,Chopper=0,ChopperJitter=0,Aperture=0,SampleVolume=1,DetectorDepth=0,DetectorArea=0,DetectionTime=0,CrystalMosaic=0" 
parameters = res_parameters +  "," + fg_parameters
simulated_vol= SimulateResolutionConvolvedModel(InputWorkspace="sr122_md",
                                             ResolutionFunction=resol_model,
                                             ForegroundModel=xsec_model,
                                             Parameters=parameters)

BinMD(InputWorkspace="simulated_vol", OutputWorkspace="simulated_vol_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')
mt_volume_table=QueryMDWorkspace('simulated_vol_cut')
mt_volume_sim=ConvertTableToMatrixWorkspace('mt_volume_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

## Mosaic ##
res_parameters = "MCLoopMin=10,MCLoopMax=10,MCType=1,Moderator=0,Chopper=0,ChopperJitter=0,Aperture=0,SampleVolume=0,DetectorDepth=0,DetectorArea=0,DetectionTime=0,CrystalMosaic=1" 
parameters = res_parameters +  "," + fg_parameters
simulated_mosaic= SimulateResolutionConvolvedModel(InputWorkspace="sr122_md",
                                             ResolutionFunction=resol_model,
                                             ForegroundModel=xsec_model,
                                             Parameters=parameters)

BinMD(InputWorkspace="simulated_mosaic", OutputWorkspace="simulated_mosaic_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')
mt_mosaic_table=QueryMDWorkspace('simulated_mosaic_cut')
mt_mosaic_sim=ConvertTableToMatrixWorkspace('mt_mosaic_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')
