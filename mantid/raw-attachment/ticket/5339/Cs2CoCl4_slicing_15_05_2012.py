from mantidsimple import*

def load_van(i):
	LoadRaw(Filename='/babylon/Public/Gosuly/Cs2CoCl4_March_2012/Raw_data/WISH000'+str(i)+'.raw',OutputWorkspace=str(i),LoadLogFiles='0',LoadMonitors='Include')
	NormaliseToMonitor(InputWorkspace=str(i),OutputWorkspace=str(i),MonitorID='4',IntegrationRangeMin='30000',IntegrationRangeMax='80000')
	CropWorkspace(InputWorkspace=str(i),OutputWorkspace=str(i),XMin='6000',XMax='99000',StartWorkspaceIndex=5)
	Rebin(InputWorkspace=str(i),OutputWorkspace=str(i),Params='6000,-0.004,99900')
	SmoothNeighbours(InputWorkspace=str(i),OutputWorkspace=str(i)+'sn',RadiusUnits='NumberOfPixels',Radius='3',NumberOfNeighbours='25',PreserveEvents='0')
	SmoothData(InputWorkspace=str(i)+'sn',OutputWorkspace=str(i)+'sn-smooth',NPoints='50')

def load_run(i):
	LoadRaw(Filename='/archive/ndxwish/Instrument/data/cycle_12_1/WISH000'+str(i)+'.raw',OutputWorkspace=str(i),LoadLogFiles='0',LoadMonitors='Include')
	NormaliseToMonitor(InputWorkspace=str(i),OutputWorkspace=str(i),MonitorID='4',IntegrationRangeMin='30000',IntegrationRangeMax='80000')
	CropWorkspace(InputWorkspace=str(i),OutputWorkspace=str(i),XMin='6000',XMax='99000',StartWorkspaceIndex=5)
	Rebin(InputWorkspace=str(i),OutputWorkspace=str(i),Params='6000,-0.004,99900')
	SmoothNeighbours(InputWorkspace=str(i),OutputWorkspace=str(i)+'sn',RadiusUnits='NumberOfPixels',Radius='3',NumberOfNeighbours='25',PreserveEvents='0')
	
	
def slicing_unbgr(vanno,runno):
	#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Divide by Vanadium
	Divide(LHSWorkspace=str(runno)+'sn',RHSWorkspace=str(vanno)+'sn-smooth',OutputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth')
	ReplaceSpecialValues(InputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth',OutputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth',NaNValue='0',InfinityValue='100000',BigNumberThreshold='99000')

	# Prepare subtracted data for VATES + look at the data - no bgr subtraction
	LoadIsawUB(InputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth',Filename=r'/babylon/Public/Gosuly/Cs2CoCl4_March_2012/CsCoCl_rot51pt6.txt')
	mtd[str(runno)+'_div_'+str(vanno)+'_sn_smooth'].setDistribution(False)
	ConvertToDiffractionMDWorkspace(InputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth',OutputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth'+'_MD_HKL',OutputDimensions='HKL')

	# for runs without bgr subtraction
	BinToMDHistoWorkspace(InputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth_MD_HKL',AlignedDim0='H,-0.53,-0.327,1',AlignedDim1='K,-1.525,1.525,120',AlignedDim2='L,2.2,3.7,1',OutputWorkspace='cut1_'+str(runno))
	#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def slicing_bgr(vanno,runno,runno_bgr):
	#######################################################################################################################################################################
	# Divide by Vanadium
	Divide(LHSWorkspace=str(runno)+'sn',RHSWorkspace=str(vanno)+'sn-smooth',OutputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth')
	ReplaceSpecialValues(InputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth',OutputWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth',NaNValue='0',InfinityValue='100000',BigNumberThreshold='99000')

	Divide(LHSWorkspace=str(runno_bgr)+'sn',RHSWorkspace=str(vanno)+'sn-smooth',OutputWorkspace=str(runno_bgr)+'_div_'+str(vanno)+'_sn_smooth')
	ReplaceSpecialValues(InputWorkspace=str(runno_bgr)+'_div_'+str(vanno)+'_sn_smooth',OutputWorkspace=str(runno_bgr)+'_div_'+str(vanno)+'_sn_smooth',NaNValue='0',InfinityValue='100000',BigNumberThreshold='99000')

	# Subtract Background
	Minus(LHSWorkspace=str(runno)+'_div_'+str(vanno)+'_sn_smooth',RHSWorkspace=str(runno_bgr)+'_div_'+str(vanno)+'_sn_smooth',OutputWorkspace=str(runno)+'minus'+str(runno_bgr)+'_smooth')

	# Prepare subtracted data for VATES + look at the data - bgr subtraction
	LoadIsawUB(InputWorkspace=str(runno)+'minus'+str(runno_bgr)+'_smooth',Filename=r'/babylon/Public/Gosuly/Cs2CoCl4_March_2012/CsCoCl_rot51pt6.txt')
	mtd[str(runno)+'minus'+str(runno_bgr)+'_smooth'].setDistribution(False)
	ConvertToDiffractionMDWorkspace(InputWorkspace=str(runno)+'minus'+str(runno_bgr)+'_smooth',OutputWorkspace=str(runno)+'minus'+str(runno_bgr)+'_smooth'+'_MD_HKL',OutputDimensions='HKL')

	#BinToMDHistoWorkspace(InputWorkspace=str(runno)+'minus'+str(runno_bgr)+'_smooth_MD_HKL',AlignedDimX='H,-2.0,2.0,120',AlignedDimY='K,-1.525,1.525,120',AlignedDimZ='L,0.025,6.025,120',OutputWorkspace='test_rebin_'+str(runno)+'minus'+str(runno_bgr))
	# for runs with bgr subtraction
	BinToMDHistoWorkspace(InputWorkspace=str(runno)+'minus'+str(runno_bgr)+'_smooth_MD_HKL',AlignedDim0='H,-0.53,-0.327,1',AlignedDim1='K,-1.525,1.525,120',AlignedDim2='L,2.06,4.45,1',OutputWorkspace='cut_'+str(runno)+'minus'+str(runno_bgr))

	# Integrate over K to get area
	BinToMDHistoWorkspace(InputWorkspace=str(runno)+'minus'+str(runno_bgr)+'_smooth_MD_HKL',AlignedDim0='H,-0.53,-0.327,1',AlignedDim1='K,0.25,0.75,1',AlignedDim2='L,2.06,4.45,1',OutputWorkspace='cut_'+str(runno)+'minus'+str(runno_bgr)+'area')
	########################################################################################################################################################################

############	
vanno = 18589
load_van(vanno)

runno_bgr = 21103
load_run(runno_bgr)

# unsubtracted background
for runno in range(21139,21146):
	load_run(runno)
	slicing_unbgr(vanno,runno)

# subtract background
for runno in range('','',''):
	load_run(runno)
	load_run(runno_bgr)
	slicing_bgr(vanno,runno)






