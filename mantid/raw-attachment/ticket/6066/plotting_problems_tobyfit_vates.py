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
eta_sig = 4.0
 
data_dir = '/data/Software/VATES_testing/Sr122_tests/'
 
## 
## A fake data set for simulation purposes.
##
fake_data = CreateSimulationWorkspace(Instrument='MERLIN',BinParams=bins,UnitX='DeltaE',
                                      DetectorTableFilename=data_dir+'MER04466.raw')

##
## Required log entries, can be taken from real ones by placing an instrument parameter of the same
## name pointing to the log name
##
AddSampleLog(Workspace=fake_data, LogName='Ei',LogText=str(ei), LogType="Number")
AddSampleLog(Workspace=fake_data, LogName='temperature_log',LogText=str(temperature), LogType="Number")
AddSampleLog(Workspace=fake_data, LogName='chopper_speed_log',LogText=str(chopper_speed), LogType="Number")
AddSampleLog(Workspace=fake_data, LogName='eta_sigma',LogText=str(eta_sig), LogType="Number")
 
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
                   Parameters="AngularVelocity=chopper_speed_log,ChopperRadius=0.049,SlitThickness=0.0023,SlitRadius=1.3,Ei=Ei,JitterSigma=0.0")
 
##
## UB matrix
##
SetUB(Workspace=fake_data,a=alatt,b=blatt,c=clatt,u=uvec,v=vvec)
 
##
## Sample rotation. Simulate 1 run at zero degrees psi
##

psi = 0.0
AddSampleLog(Workspace=fake_data,LogName='psi',LogText=str(psi),LogType='Number')
SetGoniometer(Workspace=fake_data,Axis0="psi,0,1,0,1")

# Create the MD workspace
qscale = 'Q in A^-1'
fake_md = ConvertToMD(InputWorkspace=fake_data, QDimensions="Q3D", QConversionScales=qscale,SplitInto=[3], SplitThreshold=100,
		      MinValues="-15,-15,-15,-30", MaxValues="25,25,25,279",OverwriteExisting=True)

# Run the simulation. The output is combined for each rotation into the simulated
if mtd.doesExist("simulated"):
	DeleteWorkspace("simulated")
resol_model = "TobyFitResolutionModel"
xsec_model = "Strontium122"
parameters = "Seff=0.7,J1a=38.7,J1b=-5.0,J2=27.3,SJc=10.0,GammaSlope=0.08,MultEps=0,TwinType=0,MCLoopMin=100,MCLoopMax=100"
simulated = SimulateResolutionConvolvedModel(InputWorkspace=fake_md,
					ResolutionFunction=resol_model,
					ForegroundModel=xsec_model,
					Parameters=parameters)
 

simulated_file = data_dir + 'mer300meV_sim_mantid_0deg.nxs'

#Now make some plots (or not...)

#2d:
BinMD(InputWorkspace="simulated", OutputWorkspace="simulated_slice",
		AlignedDim0='[H,0,0], -12.000000, 9.000000, 100',
		AlignedDim1='[0,K,0], -6.000000, 7.000000, 100',
		AlignedDim2='[0,0,L], -6.000000, 6.000000, 1',
		AlignedDim3='DeltaE, 100.000000, 150.000000, 1')

sv=plotSlice("simulated_slice",normalization=0)	
#If we try to use the line viewer to take a cut from this, we get the error I described previously. I have shown Alex this as well, so he knows more details if you need them

#1d:
BinMD(InputWorkspace="simulated", OutputWorkspace="simulated_cut",
		AlignedDim0='[H,0,0], -12.000000, 9.000000, 100',
		AlignedDim1='[0,K,0], -0.2, 0.2, 1',
		AlignedDim2='[0,0,L], -6.000000, 6.000000, 1',
		AlignedDim3='DeltaE, 100.000000, 150.000000, 1')

#If we then right click on the simulated_cut workspace and plotMD, then we get an empty plot. But if we list the data, we see that there is something there.
#Could this be something to do with the fact that all of the errorbars are zero, whether the signal is non-zero or not? Or something else?


#Now look at the Tobyfit sim (which has been done with mc_loop_min = mc_loop_max = 100, as above, with Sobol random number generator)
LoadSQW(Filename=data_dir + 'sr122_300meV_sim_psi0.sqw',OutputWorkspace='sr122')

#2d
BinMD(InputWorkspace='sr122',
		AlignedDim0=r'Q_\zeta, -12.000000, 9.000000, 100',
		AlignedDim1=r'Q_\xi, -6.000000, 7.000000, 100',
		AlignedDim2=r'Q_\eta, -6.000000, 6.000000, 1',
		AlignedDim3='E, 100.000000, 150.000000, 1',
		OutputWorkspace='sr122_visual_md')
		
sv_tf=plotSlice("sr122_visual_md",normalization=0)			
		
#1d
BinMD(InputWorkspace='sr122',
		AlignedDim0=r'Q_\zeta, -12.000000, 9.000000, 100',
		AlignedDim1=r'Q_\xi, -0.2, 0.2, 1',
		AlignedDim2=r'Q_\eta, -6.000000, 6.000000, 1',
		AlignedDim3='E, 100.000000, 150.000000, 1',
		OutputWorkspace='sr122_visual_md_cut')
#We are still unable to plot this, but notice on inspection of the listed data that errorbars are NOT zero - have finite (but small) errorbar when signal is non-zero.				

#In any case, we can make a comparison using table workspaces:
MinusMD("sr122_visual_md_cut","simulated_cut",OutputWorkspace="testminus")
DivideMD("testminus","simulated_cut",OutputWorkspace="testdiv")
#Making a scatter plot from the resultant table workspace of testdiv, we see that the difference (where there is signal) fluctuates in the region +/-20%.

#We can do the same for the slices:
MinusMD("sr122_visual_md","simulated_slice",OutputWorkspace="testminus_slice")
DivideMD("testminus_slice","simulated_slice",OutputWorkspace="testdiv_slice")

sv_diff=plotSlice("testdiv_slice",normalization=0)

#Now the same on the whole data, then take a slice:
MinusMD("sr122","simulated",OutputWorkspace="testminus_full")
DivideMD("testminus_full","simulated",OutputWorkspace="testdiv_full")
#OK - seems we can't do that. How come?


BinMD(InputWorkspace='testminus_full',
		AlignedDim0=r'Q_\zeta, -12.000000, 9.000000, 100',
		AlignedDim1=r'Q_\xi, -6.000000, 7.000000, 100',
		AlignedDim2=r'Q_\eta, -6.000000, 6.000000, 1',
		AlignedDim3='E, 100.000000, 150.000000, 1',
		OutputWorkspace='testminus_full_rebinned')
		
sv_tf=plotSlice("testminus_full_rebinned",normalization=0)	
#Can confirm that looks the same as when we plot testmins_slice, which is something. But the difference is non-zero.


#============================================
#Now let's try to make a very small cut from both datasets, to compare pixel by pixel:

#Recall we want to use rlu in order to get same integration:
hcorr=2*math.pi/alatt
kcorr=2*math.pi/blatt
lcorr=2*math.pi/clatt

BinMD(InputWorkspace='sr122',
		AlignedDim0=r'Q_\zeta, '+str(0.98*hcorr)+', '+str( 1.02*hcorr)+' ,1',
		AlignedDim1=r'Q_\xi, '+str(-0.2*kcorr)+' , '+str(0.2*kcorr)+' , 5',
		AlignedDim2=r'Q_\eta, -20.000000, 20.000000, 1',
		AlignedDim3='E, 0, 3, 1',
		OutputWorkspace='tft_smallcut')
		
BinMD(InputWorkspace='simulated',
		AlignedDim0=r'[H,0,0], '+str(0.98*hcorr)+', '+str( 1.02*hcorr)+' ,1',
		AlignedDim1=r'[0,K,0], '+str(-0.2*kcorr)+' , '+str(0.2*kcorr)+' , 5',
		AlignedDim2=r'[0,0,L], -20.000000, 20.000000, 1',
		AlignedDim3='DeltaE, 0, 3, 1',
		OutputWorkspace='vts_smallcut')		

#Again, inspection of these shows that we do not get the same result.
#Also - it would be nice to access the exact contributing detector pixels - inspecting the (list) data for sr122 and simulated, I can't make the connection
#between the two very easily, presumably because sr122 was histogrammed rather than event mode data.

