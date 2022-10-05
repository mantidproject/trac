from mantid.simpleapi import *
import numpy as n
import os.path
import sys

def PEARL_startup(usern="matt",thiscycle='11_1'):
	global attenfile
	global currentdatadir
	global livedatadir
	global userdataprocessed
	global calfile
	global groupfile
	global vabsorbfile
	global vanfile
	global tofbinning
	global mode
	global tt_mode
	global mtdplt
	global cycle
	global instver
	import sys
#	sys.path.append('/home/'+usern+'/Scripts/')
#	import Mantid_plotting as mtdplt
#   The lines below set the default value for the rest of the focussing routines
#	currentdatadir="C:\PEARL\RAW\\"
#	currentdatadir="X:\data\cycle_11_1\\"
	currentdatadir="X:/data/cycle_13_4/"
	livedatadir="X:/data/cycle_13_4/"
#	calfile="C:\PEARL\\pearl_offset_11_2.cal"
	calfile="pearl_offset_11_2.cal"
	groupfile="pearl_group_11_2_TT88.cal"
#	groupfile="P:\Mantid\\Calibration\\test_cal_group_mods_11_1.cal"
	vabsorbfile="pearl_absorp_sphere_10mm_newinst_long.nxs"
	vanfile="van_spline_all_cycle_11_1.nxs"
	attenfile="P:\Mantid\\Attentuation\\PRL985_WC_HOYBIDE_NK_10MM_FF.OUT"
	mode="all"
	tt_mode="TT88"
	tofbinning="1500,-0.0006,19900"
	PEARL_setdatadir(currentdatadir)
	print "Raw Data in :   ", currentdatadir
	cycle=thiscycle
	instver="new2"
	userdataprocessed="P:\users\\"+"Cycle_"+thiscycle+"\\"+usern+"\\"
#	sys.path.append(userdataprocessed)
#	userdataprocessed="C:\PEARL\\"
#	PEARL_setuserdir(directory=userdataprocessed)
	print "Cycle is set to", cycle
	print "Instrument version is set to ",instver
	print "Processed Data in : ",userdataprocessed 
	print "Offset file set to :",calfile
	print "Grouping file set to :",groupfile
	print "Vanadium file is :",vanfile
	print "The default focusing mode is :",mode
	print "Time of flight binning set to :",tofbinning
	print 
	return

def PEARL_getlambdarange():
	return 0.03,6.00

def PEARL_gettofrange():
	return 150,19900	
	
	
def PEARL_getmonitorspectrum(runno):
	
	if (runno < 71009):
		if (mode == "trans"):
			mspectra=1081
		elif (mode == "all"):
			mspectra=2721
		elif (mode == "novan"):
			mspectra=2721
		else:
			print "Sorry mode not supported"
			sys.exit(0)
	else:
		mspectra=1
		
	print "Monitor spectrum is", mspectra
			
	return mspectra

def PEARL_getcycle(number):

	global cycle
	global instver
	global datadir
	
	if type(number) is int:
		runno=number
	else:
		num=number.split("_")
		runno=int(num[0])
	
	print "The run number is get cycle is", runno
	if (runno < 71009):
		cycle="10_2"
		print "cycle is set to", cycle
		instver="old"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 71084):
		cycle="11_1"
		print "cycle is set to", cycle
		instver="new"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 71991):
		cycle="11_2"
		print "cycle is set to", cycle
		instver="new"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 73064):
		cycle="11_3"
		print "cycle is set to", cycle
		instver="new"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 73984):
		cycle="11_4"
		print "cycle is set to", cycle
		instver="new"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 74757):
		cycle="11_5"
		print "cycle is set to", cycle
		instver="new"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 75552):
		cycle="12_1"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 76662):
		cycle="12_2"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 77677):
		cycle="12_3"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 78610):
		cycle="12_4"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 80073):
		cycle="12_5"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 80812):
		cycle="13_1"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 81280):
		cycle="13_2"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	elif (runno < 82317):
		cycle="13_3"
		print "cycle is set to", cycle
		instver="new2"
		datadir="X:\data\cycle_"+cycle+"\\"
		PEARL_setdatadir(datadir)
	else:
		cycle="13_4"
		print "cycle is set to", cycle
		instver="new2"
		datadir=""#r"\\isis\inst$/NDXPEARL/Instrument/data/cycle_13_4/"
		
		PEARL_setdatadir(currentdatadir)
		
		
	print "ISIS cycle is set to", cycle
	
	return
	
	
			
def PEARL_getcalibfiles():
	global calfile
	global groupfile
	global vabsorbfile
	global vanfile
	
	print "Setting calibration for cycle", cycle
	
	if (cycle=="13_4"):
		instver="new2"
		calfile="pearl_offset_13_4.cal"
		vabsorbfile="pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="pearl_group_12_1_TT88.cal"
			vanfile="van_spline_TT88_cycle_13_3.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_13_3.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_13_3.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_13_3.nxs"
	elif (cycle=="13_3"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_13_3.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_13_3.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_13_3.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_13_3.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_13_3.nxs"
	elif (cycle=="13_2"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_13_2.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_13_2.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_13_2.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_13_2.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_13_2.nxs"
	elif (cycle=="13_1"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_13_1.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_13_1.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_13_1.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_13_1.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_13_1.nxs"
	elif (cycle=="12_5"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_12_5.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_5.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_12_5.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_12_5.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_5.nxs"
	elif (cycle=="12_4"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_12_4.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_4.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_12_4.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_12_4.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_4.nxs"
	elif (cycle=="12_3"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_12_3.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_3.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_12_3.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_12_3.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_3.nxs"
	elif (cycle=="12_2"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_12_2.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_2.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_12_2.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_12_2.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_2.nxs"
	elif (cycle=="12_1"):
		instver="new2"
		calfile="P:\Mantid\\Calibration\\pearl_offset_12_1.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst2_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_1.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_12_1.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_12_1.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_12_1_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_12_1.nxs"
	elif (cycle=="11_5"):
		instver="new"
		calfile="P:\Mantid\\Calibration\\pearl_offset_11_5.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_5.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_11_5.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_11_5.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_5.nxs"
	elif (cycle=="11_4"):
		instver="new"
		calfile="P:\Mantid\\Calibration\\pearl_offset_11_4.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_4.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_11_4.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_11_4.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_4.nxs"
	elif (cycle=="11_3"):
		instver="new"
		calfile="P:\Mantid\\Calibration\\pearl_offset_11_3.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst_long.nxs"

		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_3.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_11_3.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_11_3.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_3.nxs"
	elif (cycle=="11_2"):
		instver="new"
		calfile="P:\Mantid\\Calibration\\pearl_offset_11_2.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst.nxs"
		vanfile="P:\Mantid\\Calibration\\van_spline_mods_cycle_11_2.nxs"
		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_2.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_11_2.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_11_2.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_2.nxs"
	elif (cycle=="11_1"):
		instver="new"
		calfile="P:\Mantid\\Calibration\\pearl_offset_11_2.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_newinst_11_1.nxs"
		vanfile="P:\Mantid\\Calibration\\van_spline_mods_cycle_11_1.nxs"
		if (tt_mode=="TT88"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_1.nxs"
		elif (tt_mode=="TT70"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT70.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_11_1.nxs"
		elif (tt_mode=="TT35"):
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT35.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_11_1.nxs"
		else:
			print "Sorry I don't know that Two Theta mode so assuming T88"
			groupfile="P:\Mantid\\Calibration\\pearl_group_11_2_TT88.cal"
			vanfile="P:\Mantid\\Calibration\\van_spline_TT88_cycle_11_1.nxs"
	elif (cycle=="10_2"):
		instver="old"
		calfile="P:\Mantid\\Calibration\\pearl_offset_10_2.cal"
		groupfile="P:\Mantid\\Calibration\\pearl_group_10_2.cal"
		vabsorbfile="P:\Mantid\\Calibration\\pearl_absorp_sphere_10mm_all.nxs"
		vanfile="P:\Mantid\\Calibration\\test_van_new_cycle_10_2.nxs"
	else:
		print "Sorry that cycle has not been defined yet"
	return
	
def PEARL_setdatadir(directory="C:\PEARL\RAW\\"):
	global pearl_datadir
	pearl_datadir=directory
	return

def PEARL_setattenfile(new_atten="P:\Mantid\\Attentuation\\PRL985_WC_HOYBIDE_NK_10MM_FF.OUT"):
	global attenfile
	attenfile=new_atten
	print "Set attenuation file to ",attenfile
	return
	
def PEARL_datadir():
	return pearl_datadir

def PEARL_getfilename(run_number,ext):
	global livedatadir

	if (ext[0]!='s'):
		data_dir=PEARL_datadir()
	else:
		data_dir=livedatadir
	digit=len(str(run_number))
	
	if (run_number < 71009):
		numdigits=5
#
#		filename=data_dir+"PRL"
#
		filename="PRL"
	else:
		numdigits=8
#
#		filename=data_dir+"PEARL"
#
		filename="PEARL"

	for i in range(0,numdigits-digit):
		filename=filename+"0"
    
	filename+=str(run_number)+"."+ext
	
	full_filename=filename	
#
#   Check if file exists in default data folder & if not use alternate folder stored in "datadir"...
#	
	#if (os.path.exists(full_filename) == False):

	#	print "No such file as ",full_filename,"; trying X-drive folder..."
	
	#	full_filename=datadir+filename
		
	return full_filename
	
def PearlLoad(files,ext,outname):
	
	if type(files) is int:
		infile=PEARL_getfilename(files,ext)
		print "loading ",infile,"into ",outname
		print "--DEBUGGING: ",LoadRaw.func_code.co_filename
		LoadRaw(Filename=infile,OutputWorkspace=outname,LoadLogFiles="0")
	else:
		loop=0
		num=files.split("_")
		frange=range(int(num[0]),int(num[1])+1)
		for i in frange:
			infile=PEARL_getfilename(i,ext)
			print "loading ",infile
			outwork="run"+str(i)
			LoadRaw(Filename=infile,OutputWorkspace=outwork,LoadLogFiles="0")
			loop=loop+1
			if loop == 2:
				firstwk="run"+str(i-1)
				secondwk="run"+str(i)
				Plus(LHSWorkspace=firstwk,RHSWorkspace=secondwk,OutputWorkspace=outname)
				mtd.remove(firstwk)
				mtd.remove(secondwk)
			elif loop > 2:
				secondwk="run"+str(i)
				Plus(LHSWorkspace=outname,RHSWorkspace=secondwk,OutputWorkspace=outname)
				mtd.remove(secondwk)
	return
	
def PearlLoadMon(files,ext,outname):
	
	if type(files) is int:
		infile=PEARL_getfilename(files,ext)
		mspectra=PEARL_getmonitorspectrum(files)
		print "loading ",infile,"into ",outname
		LoadRaw(Filename=infile,OutputWorkspace=outname,SpectrumMin=mspectra,SpectrumMax=mspectra,LoadLogFiles="0")
	else:
		loop=0
		num=files.split("_")
		frange=range(int(num[0]),int(num[1])+1)
		mspectra=PEARL_getmonitorspectrum(int(num[0]))
		for i in frange:
			infile=PEARL_getfilename(i,ext)
			print "loading ",infile
			outwork="mon"+str(i)
			LoadRaw(Filename=infile,OutputWorkspace=outwork,SpectrumMin=mspectra,SpectrumMax=mspectra,LoadLogFiles="0")
			loop=loop+1
			if loop == 2:
				firstwk="mon"+str(i-1)
				secondwk="mon"+str(i)
				Plus(LHSWorkspace=firstwk,RHSWorkspace=secondwk,OutputWorkspace=outname)
				mtd.remove(firstwk)
				mtd.remove(secondwk)
			elif loop > 2:
				secondwk="mon"+str(i)
				Plus(LHSWorkspace=outname,RHSWorkspace=secondwk,OutputWorkspace=outname)
				mtd.remove(secondwk)
	return
	

	
def PEARL_getmonitor(number,ext,spline_terms=20,debug=False):
  
   works="monitor"+str(number)
   PearlLoadMon(number,ext,works) 	
   ConvertUnits(InputWorkspace=works,OutputWorkspace=works,Target="Wavelength")
   lmin,lmax=PEARL_getlambdarange()
   CropWorkspace(InputWorkspace=works,OutputWorkspace=works,XMin=lmin,XMax=lmax)
   ex_regions=n.zeros((2,4))
   ex_regions[:,0]=[3.45,3.7]
   ex_regions[:,1]=[2.96,3.2]
   ex_regions[:,2]=[2.1,2.26]
   ex_regions[:,3]=[1.73,1.98]
    #ConvertToDistribution(works)
   if (debug):
	print "The masked regions are" 
	for i in range(0,4):
		print ex_regions[0,i],ex_regions[1,i]
		#x,y,z=mtdplt.getnarray(works,0)
		#p.plot(x,y)
		
   for reg in range(0,4):
			MaskBins(InputWorkspace=works,OutputWorkspace=works,XMin=ex_regions[0,reg],XMax=ex_regions[1,reg])
			 
   if (debug):
		CloneWorkspace(InputWorkspace=works,OutputWorkspace="mask")
		#x,y,z=mtdplt.getnarray(works,0)
		#p.plot(x,y)
   SplineBackground(InputWorkspace=works,OutputWorkspace=works,WorkspaceIndex=0,NCoeff=spline_terms)
   #if (debug):
		#x,y,z=mtdplt.getnarray(works,0)
		#p.plot(x,y)
		#p.show()
    #SmoothData(works,works,50)
    #ConvertFromDistribution(works)
   return works
	
	
def PEARL_read(number,ext,outname):
	PearlLoad(number,ext,outname)
	ConvertUnits(InputWorkspace=outname,OutputWorkspace=outname,Target="Wavelength")
	#lmin,lmax=WISH_getlambdarange()
	#CropWorkspace(output,output,XMin=lmin,XMax=lmax)
	monitor=PEARL_getmonitor(number,ext,spline_terms=20,debug=False)
	#NormaliseToMonitor(InputWorkspace=outname,OutputWorkspace=outname,MonitorWorkspace=monitor)
	NormaliseToMonitor(InputWorkspace=outname,OutputWorkspace=outname,MonitorWorkspace=monitor,IntegrationRangeMin=0.6,IntegrationRangeMax=5.0)
	ConvertUnits(InputWorkspace=outname,OutputWorkspace=outname,Target="TOF")
	mtd.remove(monitor)
	#ReplaceSpecialValues(output,output,NaNValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
	return	

def PEARL_align(work,focus):
	PEARL_getcalibfiles()
	AlignDetectors(InputWorkspace=work,OutputWorkspace=work,CalibrationFile=calfile) 
	#mtd.remove(work)
	return focus

def PEARL_focus(number,ext="raw",fmode="trans",ttmode="TT70",atten=True,van_norm=True,debug=False):
	global instver
	
	PEARL_getcycle(number)
	
	print "Instrument version is:",instver
	if (instver=="new2"):
		outwork=PEARL_focus_v2(number,ext,fmode,ttmode,atten,van_norm,debug)
	else:
		outwork=PEARL_focus_v1(number,ext,fmode,ttmode,atten,van_norm,debug)
	
	
	return outwork
	
def PEARL_focus_v1(number,ext="raw",fmode="trans",ttmode="TT70",atten=True,van_norm=True,debug=False):

	global mode
	global tt_mode
	tt_mode=ttmode
	mode=fmode
	PEARL_getcycle(number)
	PEARL_getcalibfiles()
	print "Focussing mode is:",mode
	print "Two theta mode is:",tt_mode
	print "Group file is", groupfile
	print "Calibration file is", calfile
	print "Tof binning", tofbinning
	work="work"
	focus="focus"
	if type(number) is int:
	 outfile=userdataprocessed+"PRL"+str(number)+".nxs"
	 gssfile=userdataprocessed+"PRL"+str(number)+".gss"
	 tof_xye_file=userdataprocessed+"PRL"+str(number)+"_tof_xye.dat"
	 d_xye_file=userdataprocessed+"PRL"+str(number)+"_d_xye.dat"
	 outwork="PRL"+str(number)
	else:
	 outfile=userdataprocessed+"PRL"+number+".nxs"
	 gssfile=userdataprocessed+"PRL"+number+".gss"
	 tof_xye_file=userdataprocessed+"PRL"+number+"_tof_xye.dat"
	 d_xye_file=userdataprocessed+"PRL"+number+"_d_xye.dat"
	
	 outwork="PRL"+number
	 
	PEARL_read(number,ext,work)
	Rebin(InputWorkspace=work,OutputWorkspace=work,Params=tofbinning)
	AlignDetectors(InputWorkspace=work,OutputWorkspace=work,CalibrationFile=calfile)
	DiffractionFocussing(InputWorkspace=work,OutputWorkspace=focus,GroupingFileName=groupfile)
	
	
	
	if (debug!=True):
		  mtd.remove(work)
		  
	for i in range(0,12):
		output="mod"+str(i+1)
		van="van"+str(i+1)
		rdata="rdata"+str(i+1)
		if (van_norm):
			print "Using vanadium file",vanfile
			LoadNexus(Filename=vanfile,OutputWorkspace=van,EntryNumber=i+1)
			ExtractSingleSpectrum(InputWorkspace=focus,OutputWorkspace=rdata,WorkspaceIndex=i)
			#ConvertUnits(van,van,"TOF")
			Rebin(InputWorkspace=van,OutputWorkspace=van,Params=tofbinning)
			ConvertUnits(InputWorkspace=rdata,OutputWorkspace=rdata,Target="TOF")
			Rebin(InputWorkspace=rdata,OutputWorkspace=rdata,Params=tofbinning)
			Divide(LHSWorkspace=rdata,RHSWorkspace=van,OutputWorkspace=output)
			CropWorkspace(InputWorkspace=output,OutputWorkspace=output,XMin=0.1)
			Scale(InputWorkspace=output,OutputWorkspace=output,Factor=10)
		else:
			print "Not Using vanadium file"
			#LoadNexus(Filename=vanfile,OutputWorkspace=van,EntryNumber=i+1)
			ExtractSingleSpectrum(InputWorkspace=focus,OutputWorkspace=rdata,WorkspaceIndex=i)
			#ConvertUnits(van,van,"TOF")
			#Rebin(van,van,tofbinning)
			ConvertUnits(InputWorkspace=rdata,OutputWorkspace=rdata,Target="TOF")
			Rebin(InputWorkspace=rdata,OutputWorkspace=output,Params=tofbinning)
			#Divide(rdata,van,output)
			CropWorkspace(InputWorkspace=output,OutputWorkspace=output,XMin=0.1)	  
	if (debug!=True):
		  mtd.remove(focus)
		  
	if (mode=="all"):
		CloneWorkspace(InputWorkspace="mod1",OutputWorkspace="bank1")
		for i in range(1,9):
			toadd="mod"+str(i+1)
			Plus(LHSWorkspace="bank1",RHSWorkspace=toadd,OutputWorkspace="bank1")
		Scale(InputWorkspace="bank1",OutputWorkspace="bank1",Factor=0.111111111111111)
		SaveGSS(InputWorkspace="bank1",Filename=gssfile,Append=False,Bank=1)
		ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="bank1",Append=False)	
		for i in range(0,3):
			tosave="mod"+str(i+10)
			SaveGSS(InputWorkspace=tosave,Filename=gssfile,Append=True,Bank=i+2)
			ConvertUnits(InputWorkspace=tosave,OutputWorkspace=tosave,Target="dSpacing")
			SaveNexus(Filename=outfile,InputWorkspace=tosave,Append=True)
		
		if (debug!=True):
			for i in range(0,12):
				output="mod"+str(i+1)
				van="van"+str(i+1)
				rdata="rdata"+str(i+1)
				mtd.remove(rdata)
				mtd.remove(van)
				mtd.remove(output)
			mtd.remove("bank1")
		  
	elif (mode=="groups"):
		CloneWorkspace(InputWorkspace="mod1",OutputWorkspace="group1")
		CloneWorkspace(InputWorkspace="mod4",OutputWorkspace="group2")
		CloneWorkspace(InputWorkspace="mod7",OutputWorkspace="group3")
		for i in range(1,3):
			toadd="mod"+str(i+1)
			Plus(LHSWorkspace="group1",RHSWorkspace=toadd,OutputWorkspace="group1")
		Scale(InputWorkspace="group1",OutputWorkspace="group1",Factor=0.333333333333)
		for i in range(1,3):
			toadd="mod"+str(i+4)
			Plus(LHSWorkspace="group2",RHSWorkspace=toadd,OutputWorkspace="group2")
		Scale(InputWorkspace="group2",OutputWorkspace="group2",Factor=0.333333333333)
		for i in range(1,3):
			toadd="mod"+str(i+7)
			Plus(LHSWorkspace="group3",RHSWorkspace=toadd,OutputWorkspace="group3")
		Scale(InputWorkspace="group3",OutputWorkspace="group3",Factor=0.333333333333)
		Plus(LHSWorkspace="group2",RHSWorkspace="group3",OutputWorkspace="group23")
		Scale(InputWorkspace="group23",OutputWorkspace="group23",Factor=0.5)
		SaveGSS(InputWorkspace="group1",Filename=gssfile,Append=False,Bank=1)
		ConvertUnits(InputWorkspace="group1",OutputWorkspace="group1",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group1",Append=False)
		SaveGSS(InputWorkspace="group2",Filename=gssfile,Append=True,Bank=2)
		ConvertUnits(InputWorkspace="group2",OutputWorkspace="group2",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group2",Append=True)
		SaveGSS(InputWorkspace="group3",Filename=gssfile,Append=True,Bank=3)
		ConvertUnits(InputWorkspace="group3",OutputWorkspace="group3",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group3",Append=True)
		SaveGSS(InputWorkspace="group23",Filename=gssfile,Append=True,Bank=4)
		ConvertUnits(InputWorkspace="group23",OutputWorkspace="group23",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group23",Append=True)
		for i in range(0,3):
			tosave="mod"+str(i+10)
			SaveGSS(InputWorkspace=tosave,Filename=gssfile,Append=True,Bank=i+5)
			ConvertUnits(InputWorkspace=tosave,OutputWorkspace=tosave,Target="dSpacing")
			SaveNexus(Filename=outfile,InputWorkspace=tosave,Append=True)
		if (debug!=True):
			for i in range(0,12):
				output="mod"+str(i+1)
				van="van"+str(i+1)
				rdata="rdata"+str(i+1)
				mtd.remove(rdata)
				mtd.remove(van)
				mtd.remove(output)
			mtd.remove("group1")
			mtd.remove("group2")
			mtd.remove("group3")
			mtd.remove("group23")
	
	elif (mode=="trans"):
		CloneWorkspace(InputWorkspace="mod1",OutputWorkspace="bank1")
		for i in range(1,9):
			toadd="mod"+str(i+1)
			Plus(LHSWorkspace="bank1",RHSWorkspace=toadd,OutputWorkspace="bank1")
		Scale(InputWorkspace="bank1",OutputWorkspace="bank1",Factor=0.111111111111111)
		if (atten):			
			ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="dSpacing")
			CloneWorkspace(InputWorkspace="bank1",OutputWorkspace=outwork+"_noatten")
			PEARL_atten("bank1","bank1")
			ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="TOF")
			
		SaveGSS(InputWorkspace="bank1",Filename=gssfile,Append=False,Bank=1)
		
		SaveFocusedXYE(InputWorkspace="bank1",Filename=tof_xye_file,Append=False,IncludeHeader=False)
		ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="dSpacing")
		SaveFocusedXYE(InputWorkspace="bank1",Filename=d_xye_file,Append=False,IncludeHeader=False)
		SaveNexus(Filename=outfile,InputWorkspace="bank1",Append=False)	

		for i in range(0,9):
			tosave="mod"+str(i+1)
			#SaveGSS(tosave,Filename=gssfile,Append=True,Bank=i+2)
			ConvertUnits(InputWorkspace=tosave,OutputWorkspace=tosave,Target="dSpacing")
			SaveNexus(Filename=outfile,InputWorkspace=tosave,Append=True)
		
		if (debug!=True):
			for i in range(0,12):
				output="mod"+str(i+1)
				van="van"+str(i+1)
				rdata="rdata"+str(i+1)
				mtd.remove(rdata)
				mtd.remove(van)
				mtd.remove(output)
			mtd.remove("bank1")
	
	elif (mode=="mods"):
		for i in range(0,12):
			output="mod"+str(i+1)
			van="van"+str(i+1)
			rdata="rdata"+str(i+1)
			if (i==0):
				SaveGSS(InputWorkspace=output,Filename=gssfile,Append=False,Bank=i+1)
				ConvertUnits(InputWorkspace=output,OutputWorkspace=output,Target="dSpacing")
				SaveNexus(Filename=outfile,InputWorkspace=output,Append=False)
			else:
				SaveGSS(InputWorkspace=output,Filename=gssfile,Append=True,Bank=i+1)
				ConvertUnits(InputWorkspace=output,OutputWorkspace=output,Target="dSpacing")
				SaveNexus(Filename=outfile,InputWorkspace=output,Append=True)
		if (debug!=True):
		  mtd.remove(rdata)
		  mtd.remove(van)
		  mtd.remove(output)	
	
	else:
		print "Sorry I don't know that mode", mode
		return
	
	LoadNexus(Filename=outfile,OutputWorkspace=outwork)
	return outwork

def PEARL_focus_v2(number,ext="raw",fmode="trans",ttmode="TT70",atten=True,van_norm=True,debug=False):

	global mode
	global tt_mode
	tt_mode=ttmode
	mode=fmode
	PEARL_getcycle(number)
	PEARL_getcalibfiles()
	print "Focussing mode is:",mode
	print "Two theta mode is:",tt_mode
	print "Group file is", groupfile
	print "Calibration file is", calfile
	print "Tof binning", tofbinning
	work="work"
	focus="focus"
	if type(number) is int:
	 outfile=userdataprocessed+"PRL"+str(number)+".nxs"
	 gssfile=userdataprocessed+"PRL"+str(number)+".gss"
	 tof_xye_file=userdataprocessed+"PRL"+str(number)+"_tof_xye.dat"
	 d_xye_file=userdataprocessed+"PRL"+str(number)+"_d_xye.dat"
	 outwork="PRL"+str(number)
	else:
	 outfile=userdataprocessed+"PRL"+number+".nxs"
	 gssfile=userdataprocessed+"PRL"+number+".gss"
	 tof_xye_file=userdataprocessed+"PRL"+number+"_tof_xye.dat"
	 d_xye_file=userdataprocessed+"PRL"+number+"_d_xye.dat"
	
	 outwork="PRL"+number
	 
	PEARL_read(number,ext,work)
	Rebin(InputWorkspace=work,OutputWorkspace=work,Params=tofbinning)
	AlignDetectors(InputWorkspace=work,OutputWorkspace=work,CalibrationFile=calfile)
	DiffractionFocussing(InputWorkspace=work,OutputWorkspace=focus,GroupingFileName=groupfile)
	
	
	
	if (debug!=True):
		  mtd.remove(work)
		  
	for i in range(0,14):
		output="mod"+str(i+1)
		van="van"+str(i+1)
		rdata="rdata"+str(i+1)
		if (van_norm):
			print "Using vanadium file",vanfile
			LoadNexus(Filename=vanfile,OutputWorkspace=van,EntryNumber=i+1)
			ExtractSingleSpectrum(InputWorkspace=focus,OutputWorkspace=rdata,WorkspaceIndex=i)
			#ConvertUnits(van,van,"TOF")
			Rebin(InputWorkspace=van,OutputWorkspace=van,Params=tofbinning)
			ConvertUnits(InputWorkspace=rdata,OutputWorkspace=rdata,Target="TOF")
			Rebin(InputWorkspace=rdata,OutputWorkspace=rdata,Params=tofbinning)
			Divide(LHSWorkspace=rdata,RHSWorkspace=van,OutputWorkspace=output)
			CropWorkspace(InputWorkspace=output,OutputWorkspace=output,XMin=0.1)
			Scale(InputWorkspace=output,OutputWorkspace=output,Factor=10)
		else:
			print "Not Using vanadium file"
			#LoadNexus(Filename=vanfile,OutputWorkspace=van,EntryNumber=i+1)
			ExtractSingleSpectrum(InputWorkspace=focus,OutputWorkspace=rdata,WorkspaceIndex=i)
			#ConvertUnits(van,van,"TOF")
			#Rebin(van,van,tofbinning)
			ConvertUnits(InputWorkspace=rdata,OutputWorkspace=rdata,Target="TOF")
			Rebin(InputWorkspace=rdata,OutputWorkspace=output,Params=tofbinning)
			#Divide(rdata,van,output)
			CropWorkspace(InputWorkspace=output,OutputWorkspace=output,XMin=0.1)	  
	if (debug!=True):
		  mtd.remove(focus)
		  
	if (mode=="all"):
		CloneWorkspace(InputWorkspace="mod1",OutputWorkspace="bank1")
		for i in range(1,9):
			toadd="mod"+str(i+1)
			Plus(LHSWorkspace="bank1",RHSWorkspace=toadd,OutputWorkspace="bank1")
		Scale(InputWorkspace="bank1",OutputWorkspace="bank1",Factor=0.111111111111111)
		SaveGSS(InputWorkspace="bank1",Filename=gssfile,Append=False,Bank=1)
		ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="bank1",Append=False)	
		for i in range(0,5):
			tosave="mod"+str(i+10)
			SaveGSS(InputWorkspace=tosave,Filename=gssfile,Append=True,Bank=i+2)
			ConvertUnits(InputWorkspace=tosave,OutputWorkspace=tosave,Target="dSpacing")
			SaveNexus(Filename=outfile,InputWorkspace=tosave,Append=True)
		
		if (debug!=True):
			for i in range(0,14):
				output="mod"+str(i+1)
				van="van"+str(i+1)
				rdata="rdata"+str(i+1)
				mtd.remove(rdata)
				mtd.remove(van)
				mtd.remove(output)
			mtd.remove("bank1")
		  
	elif (mode=="groups"):
		CloneWorkspace(InputWorkspace="mod1",OutputWorkspace="group1")
		CloneWorkspace(InputWorkspace="mod4",OutputWorkspace="group2")
		CloneWorkspace(InputWorkspace="mod7",OutputWorkspace="group3")
		for i in range(1,3):
			toadd="mod"+str(i+1)
			Plus(LHSWorkspace="group1",RHSWorkspace=toadd,OutputWorkspace="group1")
		Scale(InputWorkspace="group1",OutputWorkspace="group1",Factor=0.333333333333)
		for i in range(1,3):
			toadd="mod"+str(i+4)
			Plus(LHSWorkspace="group2",RHSWorkspace=toadd,OutputWorkspace="group2")
		Scale(InputWorkspace="group2",OutputWorkspace="group2",Factor=0.333333333333)
		for i in range(1,3):
			toadd="mod"+str(i+7)
			Plus(LHSWorkspace="group3",RHSWorkspace=toadd,OutputWorkspace="group3")
		Scale(InputWorkspace="group3",OutputWorkspace="group3",Factor=0.333333333333)
		Plus(LHSWorkspace="group2",RHSWorkspace="group3",OutputWorkspace="group23")
		Scale(InputWorkspace="group23",OutputWorkspace="group23",Factor=0.5)
		SaveGSS(InputWorkspace="group1",Filename=gssfile,Append=False,Bank=1)
		ConvertUnits(InputWorkspace="group1",OutputWorkspace="group1",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group1",Append=False)
		SaveGSS(InputWorkspace="group2",Filename=gssfile,Append=True,Bank=2)
		ConvertUnits(InputWorkspace="group2",OutputWorkspace="group2",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group2",Append=True)
		SaveGSS(InputWorkspace="group3",Filename=gssfile,Append=True,Bank=3)
		ConvertUnits(InputWorkspace="group3",OutputWorkspace="group3",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group3",Append=True)
		SaveGSS(InputWorkspace="group23",Filename=gssfile,Append=True,Bank=4)
		ConvertUnits(InputWorkspace="group23",OutputWorkspace="group23",Target="dSpacing")
		SaveNexus(Filename=outfile,InputWorkspace="group23",Append=True)
		for i in range(0,3):
			tosave="mod"+str(i+10)
			SaveGSS(InputWorkspace=tosave,Filename=gssfile,Append=True,Bank=i+5)
			ConvertUnits(InputWorkspace=tosave,OutputWorkspace=tosave,Target="dSpacing")
			SaveNexus(Filename=outfile,InputWorkspace=tosave,Append=True)
		if (debug!=True):
			for i in range(0,14):
				output="mod"+str(i+1)
				van="van"+str(i+1)
				rdata="rdata"+str(i+1)
				mtd.remove(rdata)
				mtd.remove(van)
				mtd.remove(output)
			mtd.remove("group1")
			mtd.remove("group2")
			mtd.remove("group3")
			mtd.remove("group23")
	
	elif (mode=="trans"):
		CloneWorkspace(InputWorkspace="mod1",OutputWorkspace="bank1")
		for i in range(1,9):
			toadd="mod"+str(i+1)
			Plus(LHSWorkspace="bank1",RHSWorkspace=toadd,OutputWorkspace="bank1")
		Scale(InputWorkspace="bank1",OutputWorkspace="bank1",Factor=0.111111111111111)
		if (atten):			
			ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="dSpacing")
			CloneWorkspace(InputWorkspace="bank1",OutputWorkspace=outwork+"_noatten")
			PEARL_atten("bank1","bank1")
			ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="TOF")
			
		SaveGSS(InputWorkspace="bank1",Filename=gssfile,Append=False,Bank=1)
		SaveFocusedXYE(InputWorkspace="bank1",Filename=tof_xye_file,Append=False,IncludeHeader=False)
		ConvertUnits(InputWorkspace="bank1",OutputWorkspace="bank1",Target="dSpacing")
		SaveFocusedXYE(InputWorkspace="bank1",Filename=d_xye_file,Append=False,IncludeHeader=False)
		SaveNexus(Filename=outfile,InputWorkspace="bank1",Append=False)	
		for i in range(0,9):
			tosave="mod"+str(i+1)
			#SaveGSS(tosave,Filename=gssfile,Append=True,Bank=i+2)
			ConvertUnits(InputWorkspace=tosave,OutputWorkspace=tosave,Target="dSpacing")
			SaveNexus(Filename=outfile,InputWorkspace=tosave,Append=True)
		
		if (debug!=True):
			for i in range(0,14):
				output="mod"+str(i+1)
				van="van"+str(i+1)
				rdata="rdata"+str(i+1)
				mtd.remove(rdata)
				mtd.remove(van)
				mtd.remove(output)
			mtd.remove("bank1")
	
	elif (mode=="mods"):
		for i in range(0,12):
			output="mod"+str(i+1)
			van="van"+str(i+1)
			rdata="rdata"+str(i+1)
			if (i==0):
				SaveGSS(InputWorkspace=output,Filename=gssfile,Append=False,Bank=i+1)
				ConvertUnits(InputWorkspace=output,OutputWorkspace=output,Target="dSpacing")
				SaveNexus(Filename=outfile,InputWorkspace=output,Append=False)
			else:
				SaveGSS(InputWorkspace=output,Filename=gssfile,Append=True,Bank=i+1)
				ConvertUnits(InputWorkspace=output,OutputWorkspace=output,Target="dSpacing")
				SaveNexus(Filename=outfile,InputWorkspace=output,Append=True)
		if (debug!=True):
		  mtd.remove(rdata)
		  mtd.remove(van)
		  mtd.remove(output)	
	
	else:
		print "Sorry I don't know that mode", mode
		return
	
	LoadNexus(Filename=outfile,OutputWorkspace=outwork)
	return outwork
		
	
def PEARL_createvan(van,empty,ext="raw",fmode="all",ttmode="TT88",nvanfile="P:\Mantid\\Calibration\\van_spline_all_cycle_11_1.nxs",nspline=60,absorb=True,debug=False):
	global mode
	global tt_mode
	mode=fmode
	tt_mode=ttmode
	
	PEARL_getcycle(van)
	PEARL_getcalibfiles()
	wvan="wvan"
	wempty="wempty"
	print "Creating ", nvanfile
	PEARL_read(van,"raw",wvan)
	PEARL_read(empty,"raw",wempty)
	Minus(LHSWorkspace=wvan,RHSWorkspace=wempty,OutputWorkspace=wvan)
	print "read van and empty"
	if (debug!=True):
		mtd.remove(wempty)
	
	if(absorb==True):
		print "Correcting Vanadium for absorbtion"
		ConvertUnits(InputWorkspace=wvan,OutputWorkspace=wvan,Target="Wavelength")
		print "This will create", vabsorbfile
		# Comment out 3 lines below if absorbtion file exists and uncomment the load line
		#CreateSampleShape(wvan,'<sphere id="sphere_1"> <centre x="0" y="0" z= "0" /> <radius val="0.005" /> </sphere>')
		#AbsorptionCorrection(InputWorkspace=wvan,OutputWorkspace="T",AttenuationXSection="5.08", 	ScatteringXSection="5.1",SampleNumberDensity="0.072",NumberOfWavelengthPoints="25",ElementSize="0.05")
		#SaveNexus(Filename=vabsorbfile,InputWorkspace="T",Append=False)
		LoadNexus(Filename=vabsorbfile,OutputWorkspace="T")
		RebinToWorkspace(WorkspaceToRebin=wvan,WorkspaceToMatch="T",OutputWorkspace=wvan)
		Divide(LHSWorkspace=wvan,RHSWorkspace="T",OutputWorkspace=wvan)
		if (debug!=True):
			mtd.remove("T")
	
	ConvertUnits(InputWorkspace=wvan,OutputWorkspace=wvan,Target="TOF")
	trange="100,-0.0006,19990"
	print "Cropping TOF range to ",trange
	Rebin(InputWorkspace=wvan,OutputWorkspace=wvan,Params=trange)
	#tmin,tmax=PEARL_gettofrange()
	#print "Cropping TOF range to ",tmin,tmax
	#CropWorkspace(wvan,wvan,XMin=tmin,XMax=tmax)
	if (debug==True): 
		print "About to focus"
	vanfoc="vanfoc_"+cycle
	AlignDetectors(InputWorkspace=wvan,OutputWorkspace=wvan,CalibrationFile=calfile)
	DiffractionFocussing(InputWorkspace=wvan,OutputWorkspace=vanfoc,GroupingFileName=groupfile)
	ConvertUnits(InputWorkspace=vanfoc,OutputWorkspace=vanfoc,Target="TOF")
	trange="150,-0.0006,19900"
	print "Cropping TOF range to ",trange
	Rebin(InputWorkspace=vanfoc,OutputWorkspace=vanfoc,Params=trange)
	ConvertUnits(InputWorkspace=vanfoc,OutputWorkspace=vanfoc,Target="dSpacing")
	
	if (debug!=True):
		mtd.remove(wvan)
	
	
	
	
	
	if (instver=="new2"):
		ConvertUnits(InputWorkspace=vanfoc,OutputWorkspace="vanmask",Target="dSpacing")
		if (debug!=True):
			mtd.remove(vanfoc)
		
		#remove bragg peaks before spline
		
		print "About to strip Work=0"
		StripPeaks(InputWorkspace="vanmask",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=0)
		print "About to strip Work=1"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=1)
		print "About to strip Work=2"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=2)
		print "About to strip Work=3"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=3)
		print "About to strip Work=4"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=4)
		print "About to strip Work=5"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=5)
		print "About to strip Work=6"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=6)
		print "About to strip Work=7"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=7)
		print "About to strip Work=8"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=8)
		print "About to strip Work=9"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=9)
		print "About to strip Work=10"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=10)
		print "About to strip Work=11"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=11)
		print "About to strip Work=12"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=100, Tolerance=10, WorkspaceIndex=12)
		print "About to strip Work=13"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=60, Tolerance=10, WorkspaceIndex=13)

		#run twice on low angle as peaks are very broad
		print "About to strip Work=12 (again)"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=100, Tolerance=10, WorkspaceIndex=12)
		print "About to strip Work=13 (again)"
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=60, Tolerance=10, WorkspaceIndex=13)	

		print "Finished striping-out peaks..."		
		
		if (debug!=True):
			mtd.remove("vanmask")
	
		if (debug!=True):
			print "Not in debug mode so will delete all temporary workspaces"
		
		ConvertUnits(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",Target="TOF")

		print "Starting splines..."		

		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline1",WorkspaceIndex=0,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline2",WorkspaceIndex=1,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline3",WorkspaceIndex=2,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline4",WorkspaceIndex=3,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline5",WorkspaceIndex=4,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline6",WorkspaceIndex=5,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline7",WorkspaceIndex=6,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline8",WorkspaceIndex=7,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline9",WorkspaceIndex=8,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline10",WorkspaceIndex=9,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline11",WorkspaceIndex=10,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline12",WorkspaceIndex=11,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline13",WorkspaceIndex=12,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline14",WorkspaceIndex=13,NCoeff=nspline)
		
		#ConvertUnits("spline1","spline1","TOF")
		#ConvertUnits("spline2","spline2","TOF")
		#ConvertUnits("spline3","spline3","TOF")
		#ConvertUnits("spline4","spline4","TOF")
		#ConvertUnits("spline5","spline5","TOF")
		#ConvertUnits("spline6","spline6","TOF")
		#ConvertUnits("spline7","spline7","TOF")
		#ConvertUnits("spline8","spline8","TOF")
		#ConvertUnits("spline9","spline9","TOF")
		#ConvertUnits("spline10","spline10","TOF")
		#ConvertUnits("spline11","spline11","TOF")
		#ConvertUnits("spline12","spline12","TOF")
		SaveNexus(Filename=nvanfile,InputWorkspace="spline1",Append=False)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline2",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline3",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline4",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline5",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline6",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline7",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline8",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline9",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline10",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline11",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline12",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline13",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline14",Append=True)
		if (debug!=True):
			mtd.remove("vanstrip")
			mtd.remove("spline1")
			mtd.remove("spline2")
			mtd.remove("spline3")
			mtd.remove("spline4")
			mtd.remove("spline5")
			mtd.remove("spline6")
			mtd.remove("spline7")
			mtd.remove("spline8")
			mtd.remove("spline9")
			mtd.remove("spline10")
			mtd.remove("spline11")
			mtd.remove("spline12")
			mtd.remove("spline13")
			mtd.remove("spline14")
	elif (instver=="new"):
		ConvertUnits(InputWorkspace=vanfoc,OutputWorkspace="vanmask",Target="dSpacing")
		if (debug!=True):
			mtd.remove(vanfoc)
		
		#remove bragg peaks before spline
		StripPeaks(InputWorkspace="vanmask",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=0)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=1)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=2)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=3)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=4)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=5)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=6)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=7)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=8)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=9)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=10)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=8, WorkspaceIndex=11)
			
		if (debug!=True):
			mtd.remove("vanmask")
	
		if (debug!=True):
			print "Not in debug mode so will delete all temporary workspaces"
		
		ConvertUnits(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",Target="TOF")
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline1",WorkspaceIndex=0,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline2",WorkspaceIndex=1,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline3",WorkspaceIndex=2,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline4",WorkspaceIndex=3,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline5",WorkspaceIndex=4,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline6",WorkspaceIndex=5,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline7",WorkspaceIndex=6,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline8",WorkspaceIndex=7,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline9",WorkspaceIndex=8,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline10",WorkspaceIndex=9,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline11",WorkspaceIndex=10,NCoeff=nspline)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline12",WorkspaceIndex=11,NCoeff=nspline)
		#ConvertUnits("spline1","spline1","TOF")
		#ConvertUnits("spline2","spline2","TOF")
		#ConvertUnits("spline3","spline3","TOF")
		#ConvertUnits("spline4","spline4","TOF")
		#ConvertUnits("spline5","spline5","TOF")
		#ConvertUnits("spline6","spline6","TOF")
		#ConvertUnits("spline7","spline7","TOF")
		#ConvertUnits("spline8","spline8","TOF")
		#ConvertUnits("spline9","spline9","TOF")
		#ConvertUnits("spline10","spline10","TOF")
		#ConvertUnits("spline11","spline11","TOF")
		#ConvertUnits("spline12","spline12","TOF")
		SaveNexus(Filename=nvanfile,InputWorkspace="spline1",Append=False)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline2",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline3",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline4",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline5",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline6",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline7",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline8",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline9",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline10",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline11",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline12",Append=True)
		if (debug!=True):
			mtd.remove("vanstrip")
			mtd.remove("spline1")
			mtd.remove("spline2")
			mtd.remove("spline3")
			mtd.remove("spline4")
			mtd.remove("spline5")
			mtd.remove("spline6")
			mtd.remove("spline7")
			mtd.remove("spline8")
			mtd.remove("spline9")
			mtd.remove("spline10")
			mtd.remove("spline11")
			mtd.remove("spline12")
	elif (instver=="old"):
		ConvertUnits(InputWorkspace=vanfoc,OutputWorkspace="vanmask",Target="dSpacing")
		if (debug!=True):
			mtd.remove(vanfoc)
	
		#remove bragg peaks before spline
		StripPeaks(InputWorkspace="vanmask",OutputWorkspace="vanstrip",FWHM=15, Tolerance=6, WorkspaceIndex=0)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=6, WorkspaceIndex=2)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=15, Tolerance=6, WorkspaceIndex=3)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=40, Tolerance=12, WorkspaceIndex=1)
		StripPeaks(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",FWHM=60, Tolerance=12, WorkspaceIndex=1)
		
	
	
		if (debug!=True):
			mtd.remove("vanmask")
	
		#Mask low d region that is zero before spline
		for reg in range(0,4):
			if (reg==1):
				MaskBins(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",XMin=0,XMax=0.14, SpectraList=reg)
			else:
				MaskBins(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",XMin=0,XMax=0.06, SpectraList=reg)
	
		if (debug!=True):
			print "Not in debug mode so will delete all temporary workspaces"
		
		ConvertUnits(InputWorkspace="vanstrip",OutputWorkspace="vanstrip",Target="TOF")
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline1",WorkspaceIndex=0,NCoeff=100)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline2",WorkspaceIndex=1,NCoeff=80)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline3",WorkspaceIndex=2,NCoeff=100)
		SplineBackground(InputWorkspace="vanstrip",OutputWorkspace="spline4",WorkspaceIndex=3,NCoeff=100)
		#ConvertUnits("spline1","spline1","TOF")
		#ConvertUnits("spline2","spline2","TOF")
		#ConvertUnits("spline3","spline3","TOF")
		#ConvertUnits("spline4","spline4","TOF")
		SaveNexus(Filename=nvanfile,InputWorkspace="spline1",Append=False)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline2",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline3",Append=True)
		SaveNexus(Filename=nvanfile,InputWorkspace="spline4",Append=True)
		if (debug!=True):
			mtd.remove("vanstrip")
			mtd.remove("spline1")
			mtd.remove("spline2")
			mtd.remove("spline3")
			mtd.remove("spline4")
	else:
		print "Sorry I don't know that mode"
		return
		
	
	LoadNexus(Filename=nvanfile,OutputWorkspace="Van_data")
	
	return
	
def PEARL_createcal(calruns, noffsetfile="C:\PEARL\\pearl_offset_11_2.cal"):
	
	PEARL_getcycle(calruns)
	
	print "Instrument version is ",instver
	
	if (instver=="new2"):
		wcal="cal_raw"
		PEARL_read(calruns,"raw",wcal)
		Rebin(InputWorkspace=wcal,OutputWorkspace=wcal,Params="100,-0.0006,19950")
		ConvertUnits(InputWorkspace=wcal,OutputWorkspace="cal_inD",Target="dSpacing")	
		Rebin(InputWorkspace="cal_inD",OutputWorkspace="cal_Drebin",Params="1.8,0.002,2.1")
		CrossCorrelate(InputWorkspace="cal_Drebin",OutputWorkspace="crosscor",ReferenceSpectra=20,WorkspaceIndexMin=9,WorkspaceIndexMax=1063,XMin=1.8,XMax=2.1)
		#Ceo Cell refeined to 5.4102(3) so 220 is 1.912795
		GetDetectorOffsets(InputWorkspace="crosscor",OutputWorkspace="OutputOffsets",Step=0.002,DReference=1.912795,XMin=-200,XMax=200,GroupingFileName=noffsetfile)
		AlignDetectors(InputWorkspace=wcal,OutputWorkspace="cal_aligned",CalibrationFile=noffsetfile)
		DiffractionFocussing(InputWorkspace="cal_aligned",OutputWorkspace="cal_grouped",GroupingFileName=groupfile)
	elif (instver=="new"):
		wcal="cal_raw"
		PEARL_read(calruns,"raw",wcal)
		Rebin(InputWorkspace=wcal,OutputWorkspace=wcal,Params="100,-0.0006,19950")
		ConvertUnits(InputWorkspace=wcal,OutputWorkspace="cal_inD",Target="dSpacing")	
		Rebin(InputWorkspace="cal_inD",OutputWorkspace="cal_Drebin",Params="1.8,0.002,2.1")
		CrossCorrelate(InputWorkspace="cal_Drebin",OutputWorkspace="crosscor",ReferenceSpectra=20,WorkspaceIndexMin=9,WorkspaceIndexMax=943,XMin=1.8,XMax=2.1)
		#Ceo Cell refeined to 5.4102(3) so 220 is 1.912795
		GetDetectorOffsets(InputWorkspace="crosscor",OutputWorkspace="OutputOffsets",Step=0.002,DReference=1.912795,XMin=-200,XMax=200,GroupingFileName=noffsetfile)
		AlignDetectors(InputWorkspace=wcal,OutputWorkspace="cal_aligned",CalibrationFile=noffsetfile)
		DiffractionFocussing(InputWorkspace="cal_aligned",OutputWorkspace="cal_grouped",GroupingFileName=groupfile)
	else:
		wcal="cal_raw"
		PEARL_read(calruns,"raw",wcal)
		ConvertUnits(InputWorkspace=wcal,OutputWorkspace="cal_inD",Target="dSpacing")
		Rebin(InputWorkspace="cal_inD",OutputWorkspace="cal_Drebin",Params="1.8,0.002,2.1")
		CrossCorrelate(InputWorkspace="cal_Drebin",OutputWorkspace="crosscor",ReferenceSpectra=500,WorkspaceIndexMin=1,WorkspaceIndexMax=1440,XMin=1.8,XMax=2.1)
		#Ceo Cell refeined to 5.4102(3) so 220 is 1.912795
		GetDetectorOffsets(InputWorkspace="crosscor",OutputWorkspace="OutputOffsets",Step=0.002,DReference=1.912795,XMin=-200,XMax=200,GroupingFileName=noffsetfile)
		AlignDetectors(InputWorkspace=wcal,OutputWorkspace="cal_aligned",CalibrationFile=noffsetfile)
		DiffractionFocussing(InputWorkspace="cal_aligned",OutputWorkspace="cal_grouped",GroupingFileName=groupfile)
	
	return 
	
def PEARL_createcal_Si(calruns, noffsetfile="C:\PEARL\\pearl_offset_11_2.cal"):
	
	PEARL_getcycle(calruns)
	
	if (instver=="new2"):
		wcal="cal_raw"
		PEARL_read(calruns,"raw",wcal)
		Rebin(InputWorkspace=wcal,OutputWorkspace=wcal,Params="100,-0.0006,19950")
		ConvertUnits(InputWorkspace=wcal,OutputWorkspace="cal_inD",Target="dSpacing")
		Rebin(InputWorkspace="cal_inD",OutputWorkspace="cal_Drebin",Params="1.71,0.002,2.1")
		CrossCorrelate(InputWorkspace="cal_Drebin",OutputWorkspace="crosscor",ReferenceSpectra=20,WorkspaceIndexMin=9,WorkspaceIndexMax=1063,XMin=1.71,XMax=2.1)
		GetDetectorOffsets(InputWorkspace="crosscor",OutputWorkspace="OutputOffsets",Step=0.002,DReference=1.920127251,XMin=-200,XMax=200,GroupingFileName=noffsetfile)
		AlignDetectors(InputWorkspace=wcal,OutputWorkspace="cal_aligned",CalibrationFile=noffsetfile)
		DiffractionFocussing(InputWorkspace="cal_aligned",OutputWorkspace="cal_grouped",GroupingFileName=groupfile)
	elif (instver=="new"):
		wcal="cal_raw"
		PEARL_read(calruns,"raw",wcal)
		Rebin(InputWorkspace=wcal,OutputWorkspace=wcal,Params="100,-0.0006,19950")
		ConvertUnits(InputWorkspace=wcal,OutputWorkspace="cal_inD",Target="dSpacing")
		Rebin(InputWorkspace="cal_inD",OutputWorkspace="cal_Drebin",Params="1.85,0.002,2.05")
		CrossCorrelate(InputWorkspace="cal_Drebin",OutputWorkspace="crosscor",ReferenceSpectra=20,WorkspaceIndexMin=9,WorkspaceIndexMax=943,XMin=1.85,XMax=2.05)
		GetDetectorOffsets(InputWorkspace="crosscor",OutputWorkspace="OutputOffsets",Step=0.002,DReference=1.920127251,XMin=-200,XMax=200,GroupingFileName=noffsetfile)
		AlignDetectors(InputWorkspace=wcal,OutputWorkspace="cal_aligned",CalibrationFile=noffsetfile)
		DiffractionFocussing(InputWorkspace="cal_aligned",OutputWorkspace="cal_grouped",GroupingFileName=groupfile)
	else:
		wcal="cal_raw"
		PEARL_read(calruns,"raw",wcal)
		ConvertUnits(InputWorkspace=wcal,OutputWorkspace="cal_inD",Target="dSpacing")
		Rebin(InputWorkspace="cal_inD",OutputWorkspace="cal_Drebin",Params="3,0.002,3.2")
		CrossCorrelate(InputWorkspace="cal_Drebin",OutputWorkspace="crosscor",ReferenceSpectra=500,WorkspaceIndexMin=1,WorkspaceIndexMax=1440,XMin=3,XMax=3.2)
		GetDetectorOffsets(InputWorkspace="crosscor",OutputWorkspace="OutputOffsets",Step=0.002,DReference=1.920127251,XMin=-200,XMax=200,GroupingFileName=noffsetfile)
		AlignDetectors(InputWorkspace=wcal,OutputWorkspace="cal_aligned",CalibrationFile=noffsetfile)
		DiffractionFocussing(InputWorkspace="cal_aligned",OutputWorkspace="cal_grouped",GroupingFileName=groupfile)
	
	return 	
	
def PEARL_creategroup(calruns, ngroupfile="C:\PEARL\\test_cal_group_11_1.cal", ngroup="bank1,bank2,bank3,bank4"):
	
	wcal="cal_raw"
	PEARL_read(calruns,"raw",wcal)
	ConvertUnits(InputWorkspace=wcal,OutputWorkspace="cal_inD",Target="dSpacing")
	CreateCalFileByNames(InstrumentWorkspace=wcal,GroupingFileName=ngroupfile,GroupNames=ngroup)
	return 
	
	
def PEARL_sumspec(number,ext,mintof=500,maxtof=1000,minspec=0,maxspec=943):

	PEARL_getcycle(number)
	if (instver=="old"):
		maxspec=2720
	elif (instver=="new"):
		maxspec=943
	else:
		maxspec=1063
	
	PearlLoad(number,ext,"work")
	NormaliseByCurrent(InputWorkspace="work",OutputWorkspace="work")
	Integration(InputWorkspace="work",OutputWorkspace="integral",RangeLower=mintof,RangeUpper=maxtof,StartWorkspaceIndex=minspec,EndWorkspaceIndex=maxspec)
	mtd.remove("work")
	#sumplot=plotBin("integral",0)
	return 
	
def PEARL_sumspec_lam(number,ext,minlam=0.1,maxlam=4,minspec=8,maxspec=943):

	PEARL_getcycle(number)
	if (instver=="old"):
		maxspec=2720
	elif (instver=="new"):
		maxspec=943
	else:
		maxspec=1063
	
	PearlLoad(number,ext,"work")
	NormaliseByCurrent(InputWorkspace="work",OutputWorkspace="work")
	AlignDetectors(InputWorkspace="work",OutputWorkspace="work",CalibrationFile=calfile)
	ConvertUnits(InputWorkspace="worl",OutputWorkspace="work",Target="Wavelength")
	Integration(InputWorkspace="work",OutputWorkspace="integral",RangeLower=minlam,RangeUpper=maxlam,StartWorkspaceIndex=minspec,EndWorkspaceIndex=maxspec)
	mtd.remove("work")
	#sumplot=plotBin("integral",0)
	return 
	
def PEARL_atten(work,outwork,debug=False):
	
	#attenfile="P:\Mantid\\Attentuation\\PRL985_WC_HOYBIDE_NK_10MM_FF.OUT"
	print "Correct for attenuation using", attenfile
	wc_atten=PearlMCAbsorption(attenfile)
	ConvertToHistogram(InputWorkspace="wc_atten",OutputWorkspace="wc_atten")
	RebinToWorkspace(WorkspaceToRebin="wc_atten",WorkspaceToMatch=work,OutputWorkspace="wc_atten")
	Divide(LHSWorkspace=work,RHSWorkspace="wc_atten",OutputWorkspace=outwork)
	if (debug!=True):
			mtd.remove("wc_atten")
	return 
	
def PEARL_add(a_name,a_spectra,a_outname,atten=True):
	
	w_add_out=a_outname
	gssfile=userdataprocessed+a_outname+".gss"
	nxsfile=userdataprocessed+a_outname+".nxs"
	
	loop=0
	for i in a_spectra[:]:
		loop=loop+1
		if loop ==1:
			w_add1="PRL"+a_name+"_"+str(i)
		elif loop ==2: 
			w_add2="PRL"+a_name+"_"+str(i)
			Plus(LHSWorkspace=w_add1,RHSWorkspace=w_add2,OutputWorkspace=w_add_out)
		else:
			w_add2="PRL"+a_name+"_"+str(i)
			Plus(LHSWorkspace=w_add_out,RHSWorkspace=w_add2,OutputWorkspace=w_add_out)
	if (atten):						
			PEARL_atten(w_add_out,w_add_out)
		
	SaveNexus(Filename=nxsfile,InputWorkspace=w_add_out,Append=False)
	ConvertUnits(InputWorkspace=w_add_out,OutputWorkspace=w_add_out,Target="TOF")
	SaveGSS(InputWorkspace=w_add_out,Filename=gssfile,Append=False,Bank=i+1)
	ConvertUnits(InputWorkspace=w_add_out,OutputWorkspace=w_add_out,Target="dSpacing")
	
	return 