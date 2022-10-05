#Script to perform data reduction for MAPS

from qtiGenie import *
import time

#instrument name:
inst='mer'
iliad_setup(inst)
ext='.raw'

#map file
mapfile='/usr/local/mprogs/Libisis/InstrumentFiles/merlin/one2one_084' #single crystal mapping file
mv_mapfile='/usr/local/mprogs/Libisis/InstrumentFiles/merlin/mono_van_map'

# latest white beam vanadium file for bad detector diagnosis
wbvan=3763


#Run numbers can be specified as a list:
#runno=[17422,17423, etc]
runno=[4466]

monovan=[4581]

sam_rmm=5.433
sam_mass=349.15

#Incident energy list e.g. ei=[20,30,40]
ei=[300]

#Lo,step,hi for energy bins of output. Needs to be an array of arrays if more than one Ei used.
rebin_pars=[[-30,3,279]]

	
for i in range(len(runno)):
	#w1=iliad_abs(wbvan,runno[i],monovan[i],wbvan,sam_rmm,sam_mass,ei[i],str(rebin_pars[i]).strip('[]'),mapfile,mv_mapfile,bkgd_range=[14000,19000],diag_remove_zero=False,save_format='None')
	w1=iliad(wbvan,runno[i],ei[i],str(rebin_pars[i]).strip('[]'),mapfile,bkgd_range=[14000,19000],diag_remove_zero=False,save_format='None')
	#save_file=inst+str(runno[i])+'_ei'+str(ei[i])+'.spe'
	#SaveSPE('w1',save_file)
	#save_file=inst+str(runno[i])+'_ei'+str(ei[i])+'.nxspe'
	#SaveNXSPE('w1',save_file)




