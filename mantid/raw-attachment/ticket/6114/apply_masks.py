import numpy as np

run ='9356'

mask_folder = '/SNS/SNAP/IPTS-6996/shared/Masks/'

cal_file = '/SNS/SNAP/IPTS-6996/shared/calibration/SNAP_calibrate_d9352_2012_10_24.cal'

#The naming convention for the masks was "mask_0_5.xml" where "0_5" is the frame that STARTS at 0.5 d_spacing , note the underscore instead of dot

scales = dict(zip(['0.5','0.6','0.7','0.8','0.9','1.0','1.1','1.2','1.3','1.4','1.5','1.6','1.7','1.8','1.9','2.0','2.1'], [1.008757, 1.024455, 1.031911, 1.054462, 1.002775, 1.007764, 1.014643, 1.077643, 1.049419, 1.029146, 1.00,1.00,1.00,1.00,1.00,1.00,1.00]))

initial_range = 0.5
final_diamond_range = 2.1
final_range = 4.0
step  = 0.005

masking_step = 0.1

# I need to make masks "masking = 0"; I already made masks =  "masking = 1"
masking = 1




#My naming convention was "mask_0_5.xml" where "0_5" is the frame that STARTS at 0.5, note the underscore instead of dot
#you should not need to edit below here



bin_params = str(initial_range)+','+str(step)+','+str(final_range)

### run this part to generate summed neighbors to define masks ####################



while 1:
	if masking == 1 : break
	LoadSNSEventNexus(Filename=run ,OutputWorkspace='data_%s' %run)
	CompressEvents(InputWorkspace='data_%s' %run,OutputWorkspace='data_%s' %run)
	AlignDetectors(InputWorkspace='data_%s' %run, CalibrationFile= cal_file, OutputWorkspace='data_d_%s' %run)
	Rebin(InputWorkspace='data_d_%s' %run,OutputWorkspace='data_d_%s' %run,Params=bin_params,PreserveEvents='1') 
	SumSpectra(Inputworkspace='data_d_%s' %run, OutputWorkspace='raw_run_%s'%run)
	SumNeighbours(InputWorkspace='data_d_%s' %run,OutputWorkspace='data_d_8_%s' %run,SumX='8',SumY='8')
	Rebin(InputWorkspace='data_d_8_%s' %run,OutputWorkspace='data_d_8_%s' %run,Params=bin_params,PreserveEvents='0') 




	for d_range in np.arange(initial_range, final_diamond_range+masking_step, masking_step):
		print d_range, d_range+masking_step
		binning='%s,%s, %s' %(d_range, step, d_range+masking_step)
		Rebin(InputWorkspace='data_d_8_%s' %run, Params=binning, OutputWorkspace='data_d_8_%s_%s' %(run, d_range))
		SumSpectra(Inputworkspace='data_d_8_%s_%s' %(run, d_range), OutputWorkspace='data_d_8_%s_%s_sum' %(run, d_range))
		
	break

### run this part to load and apply  the masks ####################

LoadSNSEventNexus(Filename=run ,OutputWorkspace='data_%s' %run)
CompressEvents(InputWorkspace='data_%s' %run,OutputWorkspace='data_%s' %run)
AlignDetectors(InputWorkspace='data_%s' %run, CalibrationFile= cal_file, OutputWorkspace='data_d_%s' %run)
Rebin(InputWorkspace='data_d_%s' %run,OutputWorkspace='data_d_%s' %run,Params=bin_params,PreserveEvents='0') 
SumSpectra(Inputworkspace='data_d_%s' %run, OutputWorkspace='raw_run_%s'%run)

count = 0

#for d_range in np.arange(initial_range, final_diamond_range+masking_step, masking_step):
#	LoadMask(InputFile= mask_folder + 'mask_'+ str(d_range).replace('.','_') +'.xml', Instrument='SNAP', OutputWorkspace='mask_%s'%d_range)

for d_range in np.arange(initial_range, final_diamond_range+masking_step, masking_step):
	print d_range, d_range+masking_step
	binning='%s,%s, %s' %(d_range, step, d_range+masking_step)
	Rebin(InputWorkspace='data_d_%s' %run, Params=binning, OutputWorkspace='temp',PreserveEvents='0')
	#CloneWorkspace(InputWorkspace='temp', OutputWorkspace='pre_masked_%s'%d_range)
	LoadMask(InputFile= mask_folder + 'mask_'+ str(d_range).replace('.','_') +'.xml', Instrument='SNAP', OutputWorkspace='mask_%s'%d_range)
	MaskDetectors(Workspace='temp', MaskedWorkSpace='mask_%s'%d_range)
	#CloneWorkspace(InputWorkspace='temp', OutputWorkspace='masked_%s'%d_range)
	key='%.1f'%d_range
	Scale(InputWorkspace='temp',OutputWorkspace='temp',Factor=scales[key],Operation='Multiply')
	SumNeighbours(InputWorkspace='temp',OutputWorkspace='temp',SumX='8',SumY='8')
	#CloneWorkspace(InputWorkspace='temp', OutputWorkspace='masked_8_%s'%d_range)
	Rebin(InputWorkspace='temp', OutputWorkspace='test_d_%s'%d_range, Params=bin_params)
	if count == 0 : CloneWorkspace(InputWorkspace='test_d_%s'%d_range, OutputWorkspace='CleanOutput')
	if count != 0 : Plus(LHSWorkspace='CleanOutput',RHSWorkspace='test_d_%s'%d_range,OutputWorkspace='CleanOutput')
	SumSpectra(Inputworkspace='test_d_%s'%d_range, OutputWorkspace='test_d_%s_sum'%d_range)
	
	
	count = count+1


end_bin=str(final_diamond_range+masking_step) + ',' + str(step) + ',' + str(final_range)


SumNeighbours(InputWorkspace='data_d_%s' %run,OutputWorkspace='temp',SumX='8',SumY='8')
Rebin(InputWorkspace='temp', Params=end_bin, OutputWorkspace='temp',PreserveEvents='0')
Rebin(InputWorkspace='temp', Params=bin_params, OutputWorkspace='temp',PreserveEvents='0')
Plus(LHSWorkspace='CleanOutput',RHSWorkspace='temp',OutputWorkspace='CleanOutput')
SumSpectra(Inputworkspace='CleanOutput', OutputWorkspace='Clean_run_%s'%run)