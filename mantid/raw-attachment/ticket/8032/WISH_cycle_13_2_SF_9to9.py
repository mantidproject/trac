# Set of routines to normalise WISH data
from mantidsimple import *
import matplotlib.pyplot as p
import numpy as n
wish_dir=""

# Get the valid wavelength range, i.e. excluding regions where choppers cut 	
def WISH_getlambdarange():
	return 0.7,10.35

def WISH_setuser(usern):
	global username
	username=usern

def WISH_setdatadir(directory="/archive/ndxwish/Instrument/data/cycle_09_5/"):
	global wish_datadir
	wish_datadir=directory

def WISH_setuserdir(directory):
	global wish_userdir
	wish_userdir=directory

def WISH_datadir():
	return wish_datadir

def WISH_userdir(cycle='cycle_10_1'):
	return wish_userdir

def WISH_calibration(cycle="11_4"):
	#return "/home/mp43/Calibration/Cycle_"+cycle+"/"
	return "/home/hqs74821/work/mantid_stuff/DockWidget/"

def WISH_startup(usern,cycle='10_1'):
	global userdatadir
	global userdataprocessed
	global mtdplt
	import sys
	sys.path.append('/home/hqs74821/work/mantid_stuff/DockWidget/')
	import Mantid_plotting as mtdplt
	userdatadir="/archive/ndxwish/Instrument/data/cycle_"+cycle+'/'
	WISH_setdatadir(userdatadir)
	print "Raw Data in :   ", userdatadir	
	userdataprocessed="/home/hqs74821/work/mantid_stuff/DockWidget/ProcessedData/"
	WISH_setuserdir(directory=userdataprocessed)
	print "Processed Data in :   ",userdataprocessed 
	return


#Returns the calibration filename
def WISH_cal(panel):
	return WISH_calibration()+"WISH_cycle_10_3_noends_9to9.cal"
	
# Returns the grouping filename
def WISH_group():
	return WISH_calibration()+"WISH_cycle_10_3_noends_9to9.cal"
	
def WISH_getvana(panel,SE="candlestick",cycle="09_4"): 
	if (SE=="candlestick"):
		if (cycle=="09_2"):
			return WISH_calibration()+"vana318-"+str(panel)+"foc-rmbins-smooth50.nx5"
		if (cycle=="09_3"):
			return WISH_calibration(cycle)+"vana935-"+str(panel)+"foc-SS.nx5"
		if (cycle=="09_4"):
			return WISH_calibration(cycle)+"vana3123-"+str(panel)+"foc-SS.nx5"
		if (cycle=="09_5"):
			return WISH_calibration(cycle)+"vana3123-"+str(panel)+"foc-SS.nx5"
		if (cycle=="11_4"):
			return WISH_calibration(cycle)+"vana19612-"+str(panel)+"foc-SF-SS.nxs"	
	if (SE=="WISHcryo"):
		if (cycle=="09_2"):
			return WISH_calibration()+"vana318-"+str(panel)+"foc-rmbins-smooth50.nx5"
		if (cycle=="09_3"):
			return WISH_calibration(cycle)+"vana935-"+str(panel)+"foc-SS.nx5"
		if (cycle=="09_4"):
			return WISH_calibration(cycle)+"vana3123-"+str(panel)+"foc-SS.nx5"
		if (cycle=="11_1"):
			return WISH_calibration(cycle)+"vana17718-"+str(panel)+"foc-SS.nxs"
		if (cycle=="11_2"):
			return WISH_calibration(cycle)+"vana16812-"+str(panel)+"foc-SS.nx5"
		if (cycle=="11_3"):
			return WISH_calibration(cycle)+"vana18590-"+str(panel)+"foc-SS-new.nxs"			
			

def split_string(t):
  indxp=0
  for i in range(0,len(t)):
	if (t[i]=="+"):
		indxp=i
  if (indxp!=0):
	return int(t[0:indxp]),int(t[indxp+1:len(t)])

def WISH_getemptyinstrument(panel,cycle="09_4"):
	if (cycle=="09_4"):
		return WISH_calibration(cycle)+"emptyinst3120-"+str(panel)+"foc.nx5"

def WISH_getempty(panel,SE="WISHcryo",cycle="09_4"):
	if (SE=="WISHcryo"):
		if (cycle=="09_2"):
			return WISH_calibration(cycle)+"emptycryo322-"+str(panel)+"-smooth50.nx5"
		if (cycle=="09_3"):
			return WISH_calibration(cycle)+"emptycryo1725-"+str(panel)+"foc.nx5"
		if (cycle=="09_4"):
			return WISH_calibration(cycle)+"emptycryo3307-"+str(panel)+"foc.nx5"
		if (cycle=="09_5"):
			return WISH_calibration(cycle)+"emptycryo16759-"+str(panel)+"foc.nx5"
		if (cycle=="11_1"):
			return WISH_calibration(cycle)+"emptycryo17712-"+str(panel)+"foc-SS.nxs"
		if (cycle=="11_2"):
			return WISH_calibration(cycle)+"emptycryo16759-"+str(panel)+"foc-SS.nx5"
		if (cycle=="11_3"):
			return WISH_calibration(cycle)+"emptycryo17712-"+str(panel)+"foc-SS-new.nxs"	
		if (cycle=="11_4"):
			return WISH_calibration(cycle)+"empty_mag20620-"+str(panel)+"foc-HR-SF.nxs"			
	if (SE=="candlestick"):
		if (cycle=="09_4"):
			return WISH_calibration(cycle)+"emptyinst3120-"+str(panel)+"foc.nxs"
		if (cycle=="09_3"):
			return WISH_calibration(cycle)+"emptyinst1726-"+str(panel)+"foc-monitor.nxs"
		if (cycle=="11_4"):
			return WISH_calibration(cycle)+"emptyinst19618-"+str(panel)+"foc-SF-S.nxs"

def WISH_getfilename(run_number,ext):
	if (ext[0]!='s'):
		data_dir=WISH_datadir()
	else:
		#data_dir="/datad/ndxwish/"
		data_dir=WISH_datadir()
	digit=len(str(run_number))
	filename=data_dir+"WISH"
	for i in range(0,8-digit):
		filename=filename+"0"
	filename+=str(run_number)+"."+ext
	return filename

def WISH_returnpanel(panel):
	if (panel==1):
		min=6	
		max=19461
	elif (panel==2):
		min=19462
		max=38917
	elif( panel==3):
		min=38918
		max=58373
	elif (panel==4):
		min=58374
		max=77829
	elif (panel==5):
		min=77830
		max=97285
	elif (panel==6):
		min=97286
		max=116741
	elif (panel==7):
		min=116742
		max=136197
	elif (panel==8):
		min=136198
		max=155653	
	elif (panel==9):
		min=155654
		max=175109		
	elif (panel==0):
		min=6
		max=175109
	return min,max

# Reads a wish data file return a workspace with a short name
def WISH_read(number,panel,ext):
	if type(number) is int:
		filename=WISH_getfilename(number,ext)
		if (ext[0:9]=="nxs_event"):
			filename=WISH_getfilename(number,"nxs")
		print "will be reading filename..."+filename
		min,max=WISH_returnpanel(panel)
		if (panel!=0):
			output="w"+str(number)+"-"+str(panel)
		else:
			output="w"+str(number)
		if (ext=="raw"):
			LoadRaw(Filename=filename,OutputWorkspace=output,SpectrumMin=str(min),SpectrumMax=str(max),LoadLogFiles="0")
			MaskBins(output,output,XMin=99900,XMax=106000)
			print "standard raw file loaded"
		if (ext[0]=="s"):
			LoadRaw(Filename=filename,OutputWorkspace=output,SpectrumMin=str(min),SpectrumMax=str(max),LoadLogFiles="0")
			MaskBins(output,output,XMin=99900,XMax=106000)
			print "sav file loaded"
		if (ext=="nxs_event"):
			LoadEventNexus(Filename=filename,OutputWorkspace=output,LoadMonitors='1')
			RenameWorkspace(output+"_monitors","w"+str(number)+"_monitors")
			Rebin(InputWorkspace=output,OutputWorkspace=output,Params='6000,-0.00063,110000')
			ConvertToMatrixWorkspace(output,output)
			min,max=WISH_returnpanel(panel)
			CropWorkspace(InputWorkspace=output,OutputWorkspace=output,StartWorkspaceIndex=min-6,EndWorkspaceIndex=max-6)
			MaskBins(output,output,XMin=99900,XMax=106000)
			print "full nexus eventfile loaded"
		if (ext[0:10]=="nxs_event_"):
			label,tmin,tmax=split_string_event(ext)
			output=output+"_"+label
			if (tmax=="end"): 
			    LoadEventNexus(Filename=filename,OutputWorkspace=output,FilterByTimeStart=tmin,LoadMonitors='1',MonitorsAsEvents='1',FilterMonByTimeStart=tmin)	
			else:
			    LoadEventNexus(Filename=filename,OutputWorkspace=output,FilterByTimeStart=tmin,FilterByTimeStop=tmax,LoadMonitors='1',MonitorsAsEvents='1',FilterMonByTimeStart=tmin,FilterMonByTimeStop=tmax)
			RenameWorkspace(output+"_monitors","w"+str(number)+"_monitors")
			print "renaming monitors done!"
			Rebin(InputWorkspace=output,OutputWorkspace=output,Params='6000,-0.00063,110000')
			ConvertToMatrixWorkspace(output,output)
			min,max=WISH_returnpanel(panel)
			CropWorkspace(InputWorkspace=output,OutputWorkspace=output,StartWorkspaceIndex=min-6,EndWorkspaceIndex=max-6)
			MaskBins(output,output,XMin=99900,XMax=106000)
			print "nexus event file chopped"
		if (ext=="nxs"):
			LoadNexus(Filename=filename,OutputWorkspace=output)
			print "standard histo nxs file loaded"
	else:
		n1,n2=split_string(number)
		output="w"+str(n1)+"_"+str(n2)+"-"+str(panel)
		filename=WISH_getfilename(n1,ext)
		print "reading filename..."+filename
	        min,max=WISH_returnpanel(panel)
	        output1="w"+str(n1)+"-"+str(panel)
		LoadRaw(Filename=filename,OutputWorkspace=output1,SpectrumMin=str(min),SpectrumMax=str(max),LoadLogFiles="0")
		filename=WISH_getfilename(n2,ext)
		print "reading filename..."+filename
	        min,max=WISH_returnpanel(panel)
	        output2="w"+str(n2)+"-"+str(panel)
		LoadRaw(Filename=filename,OutputWorkspace=output2,SpectrumMin=str(min),SpectrumMax=str(max),LoadLogFiles="0")
		MergeRuns(output1+","+output2,output)
	        mantid.deleteWorkspace(output1)
		mantid.deleteWorkspace(output2)
	ConvertUnits(output,output,"Wavelength")
	lmin,lmax=WISH_getlambdarange()
	CropWorkspace(output,output,XMin=lmin,XMax=lmax)
	monitor=WISH_process_incidentmon(number,ext,spline_terms=70,debug=False)
	print "first norm to be done"
	NormaliseToMonitor(InputWorkspace=output,OutputWorkspace=output+"norm1",MonitorWorkspace=monitor)
	print "second norm to be done"
	NormaliseToMonitor(InputWorkspace=output+"norm1",OutputWorkspace=output+"norm2",MonitorWorkspace=monitor,IntegrationRangeMin=0.7,IntegrationRangeMax=10.35)
	DeleteWorkspace(output)
	DeleteWorkspace(output+"norm1")
	RenameWorkspace(output+"norm2",output)
	ConvertUnits(output,output,"TOF")
	ReplaceSpecialValues(output,output,NaNValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
	return output

#Focus dataset for a given panel and return the workspace
def WISH_focus_onepanel(work,focus,panel):
	AlignDetectors(work,work,WISH_cal(panel))
	DiffractionFocussing(work,focus,WISH_group()) 
	if (panel==5):
		CropWorkspace(focus,focus,XMin=0.3)
	mantid.deleteWorkspace(work)
	return focus

def WISH_split(focus):
	for i in range(0,10):
		out=focus[0:len(focus)-3]+"-"+str(i+1)+"foc"
		ExtractSingleSpectrum(focus,out,i)
	mantid.deleteWorkspace(focus)
	return

def WISH_focus(work,panel):
	focus=work+"foc"
	if (panel!=0):
		WISH_focus_onepanel(work,focus,panel)
	else:
		WISH_focus_onepanel(work,focus,panel)
		WISH_split(focus)

def WISH_process(number,panel,ext,SEsample="WISHcryo",emptySEcycle="09_4",SEvana="candlestick",cyclevana="09_4",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0):
	w=WISH_read(number,panel,ext)
	print "file read and normalized"
	if (absorb):
		ConvertUnits(w,w,"Wavelength")
		CylinderAbsorption(InputWorkspace=w,OutputWorkspace="T",
		CylinderSampleHeight=h,CylinderSampleRadius=r,AttenuationXSection=Xa,
		ScatteringXSection=Xs,SampleNumberDensity=nd,
		NumberOfSlices="10",NumberOfAnnuli="10",NumberOfWavelengthPoints="25",ExpMethod="Normal")
		Divide(w,"T",w)
		mantid.deleteWorkspace("T")
		ConvertUnits(w,w,"TOF")
	wfoc=WISH_focus(w,panel)
	print "focussing done!"
	if type(number) is int:
		wfocname="w"+str(number)+"-"+str(panel)+"foc"
		if (len(ext)>9): 
			label,tmin,tmax=split_string_event(ext)
			wfocname="w"+str(number)+"-"+str(panel)+"_"+label+"foc"
	else:
		n1,n2=split_string(number)
		wfocname="w"+str(n1)+"_"+str(n2)+"-"+str(panel)+"foc"
	if (panel==1):
		CropWorkspace(wfocname,wfocname,XMin=0.80,XMax=53.3)
	elif(panel==2):
		CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=13.1)
	elif(panel==3):
		CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=7.77)
	elif(panel==4):
		CropWorkspace(wfocname,wfocname,XMin=0.40,XMax=5.86)
	elif(panel==5):
		CropWorkspace(wfocname,wfocname,XMin=0.35,XMax=4.99)
	elif(panel==6):
		CropWorkspace(wfocname,wfocname,XMin=0.35,XMax=4.99)	
	elif(panel==7):
		CropWorkspace(wfocname,wfocname,XMin=0.40,XMax=5.86)	
	elif(panel==8):
		CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=7.77)	
	elif(panel==9):
		CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=13.1)		
	
	if (panel==0):
		for i in range(1,10):
			wfocname="w"+str(number)+"-"+str(i)+"foc"
			CropWorkspace(wfocname,wfocname,XMin=0.80,XMax=53.3)
			CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=13.1)
			CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=7.77)
			CropWorkspace(wfocname,wfocname,XMin=0.40,XMax=5.86)
			CropWorkspace(wfocname,wfocname,XMin=0.35,XMax=4.99)
			CropWorkspace(wfocname,wfocname,XMin=0.35,XMax=4.99)
			CropWorkspace(wfocname,wfocname,XMin=0.40,XMax=5.86)
			CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=7.77)
			CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=13.1)			
	#print "will try to load an empty with the name:"
	print WISH_getempty(panel,SEsample,emptySEcycle)
	if (panel==0):
		for i in range(1,10):
			wfocname="w"+str(number)+"-"+str(i)+"foc"
			LoadNexusProcessed(Filename=WISH_getempty(i,SEsample,emptySEcycle),OutputWorkspace="empty")
			RebinToWorkspace("empty",wfocname,"empty")
			Minus(wfocname,"empty",wfocname)
			mantid.deleteWorkspace("empty")
			print "will try to load a vanadium with the name:"+WISH_getvana(i,SEvana,cyclevana)
			LoadNexusProcessed(Filename=WISH_getvana(i,SEvana,cyclevana),OutputWorkspace="vana")	
			RebinToWorkspace("vana",wfocname,"vana")
			Divide(wfocname,"vana",wfocname)
			mantid.deleteWorkspace("vana")
			ConvertUnits(wfocname,wfocname,"TOF")
			ReplaceSpecialValues(wfocname,wfocname,NaNValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
			SaveGSS(InputWorkspace=wfocname,Filename=WISH_userdir()+str(number)+"-"+str(i)+ext+".gss",Append=False,Bank=1)
			SaveFocusedXYE(wfocname,WISH_userdir()+str(number)+"-"+str(i)+ext+".dat")
			SaveNexusProcessed(wfocname,WISH_userdir()+str(number)+"-"+str(i)+ext+".nxs") 
	else:	
		LoadNexusProcessed(Filename=WISH_getempty(panel,SEsample,emptySEcycle),OutputWorkspace="empty")
		RebinToWorkspace("empty",wfocname,"empty")
		Minus(wfocname,"empty",wfocname)
		mantid.deleteWorkspace("empty")
		print "will try to load a vanadium with the name:"+WISH_getvana(panel,SEvana,cyclevana)
		LoadNexusProcessed(Filename=WISH_getvana(panel,SEvana,cyclevana),OutputWorkspace="vana")	
		RebinToWorkspace("vana",wfocname,"vana")
		Divide(wfocname,"vana",wfocname)
		mantid.deleteWorkspace("vana")
		ConvertUnits(wfocname,wfocname,"TOF")
		ReplaceSpecialValues(wfocname,wfocname,NaNValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
		SaveGSS(InputWorkspace=wfocname,Filename=WISH_userdir()+str(number)+"-"+str(panel)+ext+".gss",Append=False,Bank=1)
		SaveFocusedXYE(wfocname,WISH_userdir()+str(number)+"-"+str(panel)+ext+".dat")
		SaveNexusProcessed(wfocname,WISH_userdir()+str(number)+"-"+str(panel)+ext+".nxs") 
	return wfocname
#Create a corrected vanadium (normalise,corrected for attenuation and empty, strip peaks) and 
# save a a nexus processed file.
# It looks like smoothing of 100 works quite well
def WISH_createvan(van,empty,panel,smoothing,vh,vr,cycle_van="09_3",cycle_empty="09_3"):
	WISH_setdatadir("/archive/ndxwish/Instrument/data/cycle_"+cycle_van+"/")
	wvan=WISH_read(van,panel,"nxs_event")
	WISH_setdatadir("/archive/ndxwish/Instrument/data/cycle_"+cycle_empty+"/")
	wempty=WISH_read(empty,panel,"nxs_event")
	Minus(wvan,wempty,wvan)
	print "read van and empty"
	mantid.deleteWorkspace(wempty)
	ConvertUnits(wvan,wvan,"Wavelength")
	CylinderAbsorption(InputWorkspace=wvan,OutputWorkspace="T",
	CylinderSampleHeight=str(vh),CylinderSampleRadius=str(vr),AttenuationXSection="4.8756",
	ScatteringXSection="5.16",SampleNumberDensity="0.07118",
	NumberOfSlices="10",NumberOfAnnuli="10",NumberOfWavelengthPoints="25",ExpMethod="Normal")
	Divide(wvan,"T",wvan)
	mantid.deleteWorkspace("T")
	ConvertUnits(wvan,wvan,"TOF")
	vanfoc=WISH_focus(wvan,panel)
	mantid.deleteWorkspace(wvan)
	#StripPeaks(vanfoc,vanfoc)
	#SmoothData(vanfoc,vanfoc,str(smoothing))
	return
	
def WISH_createempty(empty,panel):
	wempty=WISH_read(empty,panel,"raw")
	emptyfoc=WISH_focus(wempty,panel)
	return emptyfoc

def WISH_monitors(rb,ext):
	data_dir=WISH_dir()
	file=WISH_getfilename(rb,ext)
	wout="w"+str(rb)
	print "reading File..."+file
	LoadRaw(Filename=file,OutputWorkspace=wout,SpectrumMin=str(1),SpectrumMax=str(5),LoadLogFiles="0")
	NormaliseByCurrent(wout,wout)
	ConvertToDistribution(wout)
	return wout

def WISH_PH_TOF(runnumber,tubemin):
	min=6+(tubenumber-1)*128
	max=min+128
	file=WISH_getfilename(runnumber,tubemin)
	output="Run"+str(runnumber)+"tube"+str(tubenumber)
	w=WISH_read(number,panel,ext)
	print "file read and normalized"
	if (absorb):
		ConvertUnits(w,w,"Wavelength")
		CylinderAbsorption(InputWorkspace=w,OutputWorkspace="T",
		CylinderSampleHeight=h,CylinderSampleRadius=r,AttenuationXSection=Xa,
		ScatteringXSection=Xs,SampleNumberDensity=nd,
		NumberOfSlices="10",NumberOfAnnuli="10",NumberOfWavelengthPoints="25",ExpMethod="Normal")
		Divide(w,"T",w)
		mantid.deleteWorkspace("T")
		ConvertUnits(w,w,"TOF")
	wfoc=WISH_focus(w,panel)
	print "focussing done!"
	if type(number) is int:
		wfocname="w"+str(number)+"-"+str(panel)+"foc"
		if (len(ext)>9): 
			label,tmin,tmax=split_string_event(ext)
			wfocname="w"+str(number)+"-"+str(panel)+"_"+label+"foc"
	else:
		n1,n2=split_string(number)
		wfocname="w"+str(n1)+"_"+str(n2)+"-"+str(panel)+"foc"
	if (panel==1):
		CropWorkspace(wfocname,wfocname,XMin=0.80,XMax=53.3)
	elif(panel==2):
		CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=13.1)
	elif(panel==3):
		CropWorkspace(wfocname,wfocname,XMin=0.50,XMax=7.77)
	elif(panel==4):
		CropWorkspace(wfocname,wfocname,XMin=0.40,XMax=5.86)
	elif(panel==5):
		CropWorkspace(wfocname,wfocname,XMin=0.35,XMax=4.99)
	#print "will try to load an empty with the name:"
	print WISH_getempty(panel,SEsample,emptySEcycle)
	if (panel==0):
		for i in range(1,6):
			LoadNexusProcessed(Filename=WISH_getempty(i,SEsample,emptySEcycle),OutputWorkspace="empty")
			RebinToWorkspace("empty",wfocname,"empty")
			Minus(wfocname,"empty",wfocname)
			mantid.deleteWorkspace("empty")
			print "will try to load a vanadium with the name:"+WISH_getvana(i,SEvana,cyclevana)
			LoadNexusProcessed(Filename=WISH_getvana(i,SEvana,cyclevana),OutputWorkspace="vana")	
			RebinToWorkspace("vana",wfocname,"vana")
			Divide(wfocname,"vana",wfocname)
			mantid.deleteWorkspace("vana")
			ConvertUnits(wfocname,wfocname,"TOF")
#			SaveGSS(InputWorkspace=wfocname,Filename=WISH_userdir()+str(number)+"-"+str(i)+ext+".gss",Append=False,Bank=1)
#			SaveFocusedXYE(wfocname,WISH_userdir()+str(number)+"-"+str(i)+ext+".dat")
	else:	
		LoadNexusProcessed(Filename=WISH_getempty(panel,SEsample,emptySEcycle),OutputWorkspace="empty")
		RebinToWorkspace("empty",wfocname,"empty")
		Minus(wfocname,"empty",wfocname)
		mantid.deleteWorkspace("empty")
		print "will try to load a vanadium with the name:"+WISH_getvana(panel,SEvana,cyclevana)
		LoadNexusProcessed(Filename=WISH_getvana(panel,SEvana,cyclevana),OutputWorkspace="vana")	
		RebinToWorkspace("vana",wfocname,"vana")
		Divide(wfocname,"vana",wfocname)
		mantid.deleteWorkspace("vana")
		ConvertUnits(wfocname,wfocname,"TOF")
#		SaveGSS(InputWorkspace=wfocname,Filename=WISH_userdir()+str(number)+"-"+str(panel)+ext+".gss",Append=False,Bank=1)
#		SaveFocusedXYE(wfocname,WISH_userdir()+str(number)+"-"+str(panel)+ext+".dat")
	return wfocname
	LoadRaw(Filename=file,OutputWorkspace=output,spectrummin=str(min),spectrummax=str(max),LoadLogFiles="0")
	Integration(output,output+"int")
	g=plotTimeBin(output+"int",0)
	
# Smoothing the incident beam monitor using a spline function.  Regions around Bragg edges are masked, before fitting with a  spline function.
# Returns a smooth monitor spectrum


def WISH_process_incidentmon(number,ext,spline_terms=20,debug=False):
   if type(number) is int:
	fname=WISH_getfilename(number,ext)
	works="monitor"+str(number)
	if (ext=="raw"):
		works="monitor"+str(number)
		LoadRaw(Filename=fname,OutputWorkspace=works,SpectrumMin=4,SpectrumMax=4,LoadLogFiles="0")
	if (ext[0]=="s"):
		works="monitor"+str(number)
		LoadRaw(Filename=fname,OutputWorkspace=works,SpectrumMin=4,SpectrumMax=4,LoadLogFiles="0")
	if (ext=="nxs"):		
		works="monitor"+str(number)
		LoadNexus(Filename=fname,OutputWorkspace=works,SpectrumMin=4,SpectrumMax=4)
	if (ext[0:9]=="nxs_event"):
		temp="w"+str(number)+"_monitors"
		works="w"+str(number)+"_monitor4"
		Rebin(temp,temp,Params='6000,-0.00063,110000',PreserveEvents=False)
		ExtractSingleSpectrum(temp,works,3)
   else:
	n1,n2=split_string(number)
	works="monitor"+str(n1)+"_"+str(n2)
	fname=WISH_getfilename(n1,ext)
	works1="monitor"+str(n1)
	LoadRaw(Filename=fname,OutputWorkspace=works1,SpectrumMin=4,SpectrumMax=4,LoadLogFiles="0")
	fname=WISH_getfilename(n2,ext)
	works2="monitor"+str(n2)
	LoadRaw(Filename=fname,OutputWorkspace=works2,SpectrumMin=4,SpectrumMax=4,LoadLogFiles="0")
	MergeRuns(works1+","+works2,works)
	mantid.deleteWorkspace(works1)
	mantid.deleteWorkspace(works2)
   ConvertUnits(works,works,"Wavelength")
   lmin,lmax=WISH_getlambdarange()
   CropWorkspace(works,works,XMin=lmin,XMax=lmax)
   ex_regions=n.zeros((2,4))
   ex_regions[:,0]=[4.57,4.76]
   ex_regions[:,1]=[3.87,4.12]
   ex_regions[:,2]=[2.75,2.91]
   ex_regions[:,3]=[2.24,2.50]
   ConvertToDistribution(works)
   if (debug):
		x,y,z=mtdplt.getnarray(works,0)
		p.plot(x,y)
   for reg in range(0,4):
			MaskBins(works,works,XMin=ex_regions[0,reg],XMax=ex_regions[1,reg])
   if (debug):
		x,y,z=mtdplt.getnarray(works,LoadRaw0)
		p.plot(x,y)
   SplineBackground(works,works,0,spline_terms)
   if (debug):
		x,y,z=mtdplt.getnarray(works,0)
		p.plot(x,y)
   p.show()
   SmoothData(works,works,40)
   ConvertFromDistribution(works)
   return works
   
#removes the peaks in a vanadium  run, then performs a spline and a smooth
def Removepeaks_spline_smooth_empty(works,panel,debug=False):
	if (panel==1):
		splineterms=0
		smoothterms=30
	if (panel==2):
		splineterms=0
		smoothterms=10
	if (panel==3):
		splineterms=0
		smoothterms=15
	if (panel==4):
		splineterms=0
		smoothterms=15
	if (panel==5):
		splineterms=0
		smoothterms=10
	if (debug):
		x,y,z=getnarray(works,0)
		p.plot(x,y)
	if (splineterms!=0):
		SplineBackground(works,works,0,splineterms)
	if (debug):
		x,y,z=getnarray(works,0)
		p.plot(x,y)
	SmoothData(works,works,smoothterms)
	if (debug):
		x,y,z=getnarray(works,0)
		p.plot(x,y)
	p.show()
	return works

def split_string_event(t):
#this assumes the form nxs_event_label_tmin_tmax
  indx_=[]
  for i in range(10,len(t)):
	if (t[i]=="_"):
		indx_.append(i)
  label=t[10:indx_[0]]
  tmin=t[indx_[0]+1:indx_[1]]
  tmax=t[indx_[1]+1:len(t)]
  return label,tmin,tmax

#test="nxs_event_1_300.00_600.00"
#print split_string_event(test)

# #####################################################################
# #####     			USER SPECIFIC PART STARTS BELOW 									   ##
# #####     			IN CASE LINES ABOVE HAVE BEEN EDITED AND SCRIPTS NO LONGER WORK   ##
# #####     			LOG OUT AND BACK IN TO THE MACHINE								   ##
# #####################################################################
# ########### SETTING the paths automatically : WISH_startup(username,cycle_name) ##############
WISH_startup("mp43","13_3")
# #        WISH PROCESS ROUTINES TO EDIT   (penultimate line optional but useful for recovering data later on)  #
# To add two raw files together, replace runno (integer, eg. 16800) by a string "int1+int2" (eg "16800+16801" note quotes)
# ##############################################################################################
#beg=0
#end=1800
#nbslices=int(end/180)
#suffix=[]
#for k in range(0,nbslices):
#	suffix.append("nxs_event_slice"+str(k)+"_"+str(int(k*180))+"_"+str((k+1)*180))

#print len(suffix) 
#print suffix[0], suffix[k]

#for i in range(24901,24902):
#	for j in range(2,3):
#		for k in range(0,len(suffix)):
#			wout=WISH_process(i,j,suffix[k],"candlestick","11_4","candlestick","11_4",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#			ConvertUnits(wout,wout+"-d","dSpacing")
# ##############################################################################################
#for i in range(24895,24896):
#	for j in range(5,6):
#		wout=WISH_process(i,j,"nxs_event_slice1_0_300","candlestick","11_4","candlestick","11_4",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice2_300_600","candlestick","11_4","candlestick","11_4",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice3_600_900","candlestick","11_4","candlestick","11_4",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice4_900_1200","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice5_1200_1500","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice6_1500_1800","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice7_1800_2100","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice8_2100_2400","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice9_2400_2700","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice10_2700_3000","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice11_3000_3300","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		ConvertUnits(wout,wout+"-d","dSpacing")
#		wout=WISH_process(i,j,"nxs_event_slice12_3300_end","WISHcryo","11_3","WISHcryo","11_3",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)

for i in range(25449,25450):
	for j in range(1,10):
		wout=WISH_process(i,j,"raw","candlestick","11_4","candlestick","11_4",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
		ConvertUnits(wout,wout+"-d","dSpacing")
#	SaveGSS("w"+str(i)+"-1foc",WISH_userdir()+str(i)+"-1foc"+".gss",Append=False,Bank=1)
#	SaveFocusedXYE("w"+str(i)+"-1foc",WISH_userdir()+str(i)+"-1foc"+".dat")	
#	SaveGSS("w"+str(i)+"-2foc",WISH_userdir()+str(i)+"-2foc"+".gss",Append=False,Bank=1)
#	SaveFocusedXYE("w"+str(i)+"-2foc",WISH_userdir()+str(i)+"-2foc"+".dat")	
	RebinToWorkspace("w"+str(i)+"-6foc","w"+str(i)+"-5foc","w"+str(i)+"-6foc")	
	Plus("w"+str(i)+"-5foc","w"+str(i)+"-6foc","w"+str(i)+"-5_6foc")
	ConvertUnits("w"+str(i)+"-5_6foc","w"+str(i)+"-5_6foc"+"-d","dSpacing")
	SaveGSS("w"+str(i)+"-5_6foc",WISH_userdir()+str(i)+"-5_6foc"+".gss",Append=False,Bank=1)
	SaveFocusedXYE("w"+str(i)+"-5_6foc",WISH_userdir()+str(i)+"-5_6foc"+".dat")
	SaveNexusProcessed("w"+str(i)+"-5_6foc",WISH_userdir()+str(i)+"-5_6foc"+".nxs")
	RebinToWorkspace("w"+str(i)+"-7foc","w"+str(i)+"-4foc","w"+str(i)+"-7foc")
	Plus("w"+str(i)+"-4foc","w"+str(i)+"-7foc","w"+str(i)+"-4_7foc")
	ConvertUnits("w"+str(i)+"-4_7foc","w"+str(i)+"-4_7foc"+"-d","dSpacing")
	SaveGSS("w"+str(i)+"-4_7foc",WISH_userdir()+str(i)+"-4_7foc"+".gss",Append=False,Bank=1)
	SaveFocusedXYE("w"+str(i)+"-4_7foc",WISH_userdir()+str(i)+"-4_7foc"+".dat")
	SaveNexusProcessed("w"+str(i)+"-4_7foc",WISH_userdir()+str(i)+"-4_7foc"+".nxs")
	RebinToWorkspace("w"+str(i)+"-8foc","w"+str(i)+"-3foc","w"+str(i)+"-8foc")
	Plus("w"+str(i)+"-3foc","w"+str(i)+"-8foc","w"+str(i)+"-3_8foc")
	ConvertUnits("w"+str(i)+"-3_8foc","w"+str(i)+"-3_8foc"+"-d","dSpacing")
	SaveGSS("w"+str(i)+"-3_8foc",WISH_userdir()+str(i)+"-3_8foc"+".gss",Append=False,Bank=1)
	SaveFocusedXYE("w"+str(i)+"-3_8foc",WISH_userdir()+str(i)+"-3_8foc"+".dat")	
	SaveNexusProcessed("w"+str(i)+"-3_8foc",WISH_userdir()+str(i)+"-3_8foc"+".nxs")
	RebinToWorkspace("w"+str(i)+"-9foc","w"+str(i)+"-2foc","w"+str(i)+"-9foc")
	Plus("w"+str(i)+"-2foc","w"+str(i)+"-9foc","w"+str(i)+"-2_9foc")
	ConvertUnits("w"+str(i)+"-2_9foc","w"+str(i)+"-2_9foc"+"-d","dSpacing")
	SaveGSS("w"+str(i)+"-2_9foc",WISH_userdir()+str(i)+"-2_9foc"+".gss",Append=False,Bank=1)
	SaveFocusedXYE("w"+str(i)+"-2_9foc",WISH_userdir()+str(i)+"-2_9foc"+".dat")	
	SaveNexusProcessed("w"+str(i)+"-2_9foc",WISH_userdir()+str(i)+"-2_9foc"+".nxs")	
# #############################################################################################
#for i in range(23840,23841):
#	for j in range(5,0,-1):
#		wout=WISH_process(i,j,"raw","candlestick","11_4","candlestick","11_4",absorb=False,nd=0.0,Xs=0.0,Xa=0.0,h=0.0,r=0.0)
#		SaveNexusProcessed(wout,WISH_userdir()+wout+".nxs") 
#		ConvertUnits(wout,wout+"-d","dSpacing")


# ###########################################################################################
#for i in range(18880,18881):
#	for j in range(1,6):
#		wout=WISH_process(i,j,"raw","WISHcryo","11_3","WISHcryo","11_3",absorb=True,nd=0.0035,Xs=62.27,Xa=429.95,h=4.0,r=0.15)
# ###########################################################################################
# #########               END OF WISH PROCESS ROUTINES                               ##################

# #####################################################################
# How to retrieve already processed Data without having to reprocess it  (in case Mantid session has been closed #
#for runno in range(24122,24130):
# for j in range(1,6):
#	wr=str(runno)+"-"+str(j)+"raw-0"
#	LoadNexusProcessed(WISH_userdir()+wr+".nxs",wr)
#	ConvertUnits(wr,wr+"-d","dSpacing")

  #####################################################################
#for runno in range(22678,22686):
  #for j in range(1,6):
	#wr="w"+str(runno)+"-"+str(j)+"foc"

#for j in range(1,6):
#	Plus("w22663"+"-"+str(j)+"foc","w22664"+"-"+str(j)+"foc","vancan"+"-"+str(j)+"foc")
#	SaveGSS(InputWorkspace="vancan"+"-"+str(j)+"foc",Filename=WISH_userdir()+"vancan"+"-"+str(j)+"foc.gss",Append=False,Bank=1)
	
	


# ####################################################################
# If you don't have a correct empty, either use the most suitable one or use the lines below ####
#for i in range(1197,1410):
#	for j in range(1,6):
#		wout=WISH_read(i,j,"raw")
#		wfoc=WISH_focus(wout,j)
# ####################################################################
# use the lines below to manually set the paths if needed
#WISH_setdatadir("/archive/ndxwish/Instrument/data/cycle_10_1/")
#WISH_setuserdir("/home/mp43/ProcessedData/")WISHcryo
# ######### use the lines below to process a LoadRawvanadium run                               ##################
#for j in range(1,2):
#	WISH_createvan(19612,19618,j,100,4.0,0.15,cycle_van="11_4",cycle_empty="11_4")
#	CropWorkspace(InputWorkspace="w19612-"+str(j)+"foc",OutputWorkspace="w19612-"+str(j)+"foc",XMin='0.35',XMax='5.0')
#	Removepeaks_spline_smooth_vana("w18904-"+str(j)+"foc",j,debug=False)
#	SaveNexusProcessed("w16847-"+str(i)+"foc",WISH_userdir()+"vana16847-"+str(i)+"foc.nx5")
# ########  use the lines below to create a processed empty (instrument, cryostat, can..) run     ########
#for i in range(4,5):
#	WISH_createempty(20620,i)
 #SaveNexusProcessed("w16748-"+str(i)+"foc",WISH_userdir()+"emptyinst16748-"+str(i)+"foc.nx5")
  

