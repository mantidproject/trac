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
	
#===============================

#Load  the equivalent SQW files:
data_dir = '/data/Software/VATES_testing/Sr122_tests/'
#LoadSQW(Filename=data_dir + 'sr122_minimal_mantid_check_mantidpar.sqw',OutputWorkspace='sr122_tobyfit_mt')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_moderator.sqw',OutputWorkspace='sr122_tobyfit_moderator')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_aperture.sqw',OutputWorkspace='sr122_tobyfit_aperture')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_chopper.sqw',OutputWorkspace='sr122_tobyfit_chopper')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_jitter.sqw',OutputWorkspace='sr122_tobyfit_jitter')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_volume.sqw',OutputWorkspace='sr122_tobyfit_volume')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_area.sqw',OutputWorkspace='sr122_tobyfit_area')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_depth.sqw',OutputWorkspace='sr122_tobyfit_depth')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_time.sqw',OutputWorkspace='sr122_tobyfit_time')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_mosaic.sqw',OutputWorkspace='sr122_tobyfit_mosaic')
LoadSQW(Filename=data_dir + 'sr122_tobyfit_all.sqw',OutputWorkspace='sr122_tobyfit_all')


#Want to work through the sqw/tobyfit and mantid simulations to compare for each resolution component:
		
#BinMD(InputWorkspace="sr122_tobyfit_mt", OutputWorkspace="sr122_tobyfit_mt_cut",
#		AlignedDim0=r'qx, 1, 1.3, 1',
#		AlignedDim1=r'qy, -1, 1, 41',
#		AlignedDim2=r'qz, -100, 100, 1',
#		AlignedDim3='en, 65, 75, 1')		

BinMD(InputWorkspace="sr122_tobyfit_moderator", OutputWorkspace="sr122_tobyfit_moderator_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		

BinMD(InputWorkspace="sr122_tobyfit_aperture", OutputWorkspace="sr122_tobyfit_aperture_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		
		
BinMD(InputWorkspace="sr122_tobyfit_chopper", OutputWorkspace="sr122_tobyfit_chopper_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		
		
BinMD(InputWorkspace="sr122_tobyfit_jitter", OutputWorkspace="sr122_tobyfit_jitter_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		
		
BinMD(InputWorkspace="sr122_tobyfit_volume", OutputWorkspace="sr122_tobyfit_volume_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		
		
BinMD(InputWorkspace="sr122_tobyfit_area", OutputWorkspace="sr122_tobyfit_area_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		
		
BinMD(InputWorkspace="sr122_tobyfit_depth", OutputWorkspace="sr122_tobyfit_depth_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		
		
BinMD(InputWorkspace="sr122_tobyfit_time", OutputWorkspace="sr122_tobyfit_time_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')		
		
BinMD(InputWorkspace="sr122_tobyfit_mosaic", OutputWorkspace="sr122_tobyfit_mosaic_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')	

BinMD(InputWorkspace="sr122_tobyfit_all", OutputWorkspace="sr122_tobyfit_all_cut",
		AlignedDim0=r'qx, 1, 1.3, 1',
		AlignedDim1=r'qy, -1, 1, 41',
		AlignedDim2=r'qz, -100, 100, 1',
		AlignedDim3='en, 65, 75, 1')	

###############
#Mantid equivalents:

BinMD(InputWorkspace="simulated_mod", OutputWorkspace="simulated_mod_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_aperture", OutputWorkspace="simulated_aperture_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_chopper", OutputWorkspace="simulated_chopper_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_jitter", OutputWorkspace="simulated_jitter_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_vol", OutputWorkspace="simulated_vol_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_area", OutputWorkspace="simulated_area_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_depth", OutputWorkspace="simulated_depth_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_time", OutputWorkspace="simulated_time_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

BinMD(InputWorkspace="simulated_mosaic", OutputWorkspace="simulated_mosaic_cut",
		AlignedDim0='[H,0,0], 1, 1.3, 1',
		AlignedDim1='[0,K,0], -1, 1, 41',
		AlignedDim2='[0,0,L], -100, 100, 1',
		AlignedDim3='DeltaE, 65, 75.000000, 1')

#####
#Plot comparisons

all_table=QueryMDWorkspace('sr122_tobyfit_all_cut')
all_sim=ConvertTableToMatrixWorkspace('all_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

mod_table=QueryMDWorkspace('sr122_tobyfit_moderator_cut')
mod_sim=ConvertTableToMatrixWorkspace('mod_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

chop_table=QueryMDWorkspace('sr122_tobyfit_chopper_cut')
chop_sim=ConvertTableToMatrixWorkspace('chop_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

aperture_table=QueryMDWorkspace('sr122_tobyfit_aperture_cut')
aperture_sim=ConvertTableToMatrixWorkspace('aperture_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

jitter_table=QueryMDWorkspace('sr122_tobyfit_jitter_cut')
jitter_sim=ConvertTableToMatrixWorkspace('jitter_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

volume_table=QueryMDWorkspace('sr122_tobyfit_volume_cut')
volume_sim=ConvertTableToMatrixWorkspace('volume_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

area_table=QueryMDWorkspace('sr122_tobyfit_area_cut')
area_sim=ConvertTableToMatrixWorkspace('area_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

depth_table=QueryMDWorkspace('sr122_tobyfit_depth_cut')
depth_sim=ConvertTableToMatrixWorkspace('depth_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

time_table=QueryMDWorkspace('sr122_tobyfit_time_cut')
time_sim=ConvertTableToMatrixWorkspace('time_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

mosaic_table=QueryMDWorkspace('sr122_tobyfit_mosaic_cut')
mosaic_sim=ConvertTableToMatrixWorkspace('mosaic_table',ColumnX='qy/A^-1',ColumnY='Signal/none')

##########

mt_mod_table=QueryMDWorkspace('simulated_mod_cut')
mt_mod_sim=ConvertTableToMatrixWorkspace('mt_mod_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_chop_table=QueryMDWorkspace('simulated_chopper_cut')
mt_chop_sim=ConvertTableToMatrixWorkspace('mt_chop_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_ap_table=QueryMDWorkspace('simulated_aperture_cut')
mt_ap_sim=ConvertTableToMatrixWorkspace('mt_ap_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_vol_table=QueryMDWorkspace('simulated_vol_cut')
mt_vol_sim=ConvertTableToMatrixWorkspace('mt_vol_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_jitter_table=QueryMDWorkspace('simulated_jitter_cut')
mt_jitter_sim=ConvertTableToMatrixWorkspace('mt_jitter_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_area_table=QueryMDWorkspace('simulated_area_cut')
mt_area_sim=ConvertTableToMatrixWorkspace('mt_area_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_depth_table=QueryMDWorkspace('simulated_depth_cut')
mt_depth_sim=ConvertTableToMatrixWorkspace('mt_depth_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_time_table=QueryMDWorkspace('simulated_time_cut')
mt_time_sim=ConvertTableToMatrixWorkspace('mt_time_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

mt_mosaic_table=QueryMDWorkspace('simulated_mosaic_cut')
mt_mosaic_sim=ConvertTableToMatrixWorkspace('mt_mosaic_table',ColumnX='[0,K,0]/A^-1',ColumnY='Signal/none')

