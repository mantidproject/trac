#The two lines below are always needed and need to be run at least once before the other cammands will work
#They setup various enviroment variables
#from SET_env_pearl import *
from pearl_routines_13_4 import *
reload(sys.modules["pearl_routines_13_4"])
PEARL_startup("Calib","13_4")

#for irun in range(82353,82363):
#	PEARL_focus(irun,"raw",fmode="trans",ttmode="TT88",atten=False,van_norm=False,debug=False)

#PEARL_focus("82353_82362","raw",fmode="all",ttmode="TT88",atten=False,van_norm=False,debug=False)

#PEARL_focus("82350_82352","raw",fmode="all",ttmode="TT88",atten=False,van_norm=True,debug=False)
#PEARL_focus("81306_81309","raw",fmode="all",ttmode="TT88",atten=False,van_norm=True,debug=False)

#PEARL_focus(80832,"raw",fmode="all",ttmode="TT88",atten=False,van_norm=False,debug=False)
#PEARL_focus(81281,"raw",fmode="all",ttmode="TT88",atten=False,van_norm=False,debug=False)
#PEARL_focus(81287,"raw",fmode="all",ttmode="TT88",atten=False,van_norm=False,debug=False)

#PEARL_focus("80889_80897","raw",fmode="trans",ttmode="TT70",atten=False,van_norm=True,debug=False)
#PEARL_focus("80898_80902","raw",fmode="trans",ttmode="TT70",atten=False,van_norm=True,debug=False)
#PEARL_focus("80903_80909","raw",fmode="trans",ttmode="TT70",atten=False,van_norm=True,debug=False)

#
# Cycle 13/3 calibration data from standard 10mm diameter vanadium sphere target...
#
#PEARL_focus("81281_81289","raw",fmode="all",ttmode="TT35",atten=False,van_norm=False,debug=False)

#
# Empty S-E tank data...
#
#PEARL_focus("80094_80096","raw",fmode="all",ttmode="TT88",atten=False,van_norm=False,debug=False)
#PEARL_focus("81302_81305","raw",fmode="all",ttmode="TT35",atten=False,van_norm=False,debug=False)
#
# NBS Si (SRM640c); data seem OK...
#
#PEARL_focus("80851_80863","raw",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)

#PEARL_focus(81306,"s01",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)

#
# NBS CeO2 (SRM674a); data seem OK...
#
#PEARL_focus("81290_81301","raw",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)
#PEARL_focus("80864_80876","raw",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)
#PEARL_focus(80864,"raw",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)
#PEARL_focus("81290_81301","raw",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)
#PEARL_focus(81301,"raw",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)
#
# KTP sample (long d-spacings); data seem OK...
#
#PEARL_focus("82375_82381","raw",fmode="all",ttmode="TT70",atten=False,van_norm=True,debug=False)
# To create the vanadium file for a cycle use the following, where the first set of runs are the vanadium and the second are the background in each case.
newvanfile="van_spline_TT88_cycle_13_4.nxs"
PEARL_createvan("82353_82362","82342_82349",ttmode="TT88",nvanfile=newvanfile,nspline=40,absorb=True,debug=True)
#CloneWorkspace(InputWorkspace="Van_data",OutputWorkspace="van_tt88")

#newvanfile="P:\Mantid\\Calibration\\van_spline_TT70_cycle_13_4.nxs"
#PEARL_createvan("82353_82362","82342_82349",ttmode="TT70",nvanfile=newvanfile,nspline=40,absorb=True,debug=True)
#CloneWorkspace(InputWorkspace="Van_data",OutputWorkspace="van_tt70")

#newvanfile="P:\Mantid\\Calibration\\van_spline_TT35_cycle_13_4.nxs"
#PEARL_createvan("82353_82362","82342_82349",ttmode="TT35",nvanfile=newvanfile,nspline=40,absorb=True,debug=True)
#CloneWorkspace(InputWorkspace="Van_data",OutputWorkspace="van_tt35")

# To produce an offset calibration file with NBS CeO2 data use:
#offsetfile="P:\Mantid\\Calibration\\pearl_offset_13_4.cal"
#PEARL_createcal("82363_82369",noffsetfile=offsetfile)
#PEARL_createcal("81290_81301",noffsetfile=offsetfile)

# To produce an offset calibration file with NBS Si data use:
#offsetfile="P:\Mantid\\Calibration\\pearl_offset_12_5_si.cal"
#PEARL_createcal_Si("78618_78619",noffsetfile=offsetfile)

#To produce a basic grouping file use the command below. The final files need to be processing in excel to add the two theta selection.
#ngroupfile="C:\PEARL\\test_cal_group_mods_11_1.cal"
#PEARL_creategroup(71030,ngroupfile,"mod1,mod2,mod3,mod4,mod5,mod6,mod7,mod8,mod9,mod10,mod11,mod12")
