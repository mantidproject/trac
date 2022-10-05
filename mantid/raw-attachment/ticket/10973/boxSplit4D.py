import os

#----------------------------- WITHOUT INITIAL SPLITTING (woIS)-----------------------------------------------------------
# set up target ws name and remove target workspace with the same name which can occasionally exist.
# list of MD files (workspaces) to combine into target MD workspace
MD_FilesList_woIS='';

# define convetr to MD parameters
pars_woIS = dict();
pars_woIS['InputWorkspace']=''
pars_woIS['QDimensions']='Q3D'
pars_woIS['dEAnalysisMode']='Direct'
pars_woIS['Q3DFrames']='HKL'
pars_woIS['QConversionScales']='HKL'
pars_woIS['PreprocDetectorsWS']='preprDetMantid'
pars_woIS['MinValues']='-3,-3,-3.,-50.0'
pars_woIS['MaxValues']='3.,3.,3.,50.0'
pars_woIS['SplitInto']=5
pars_woIS['MaxRecursionDepth']=1
pars_woIS['MinRecursionDepth']=1
pars_woIS['OverwriteExisting']=1  # Change this to false, if the files should/can be added in memory
# test script combines all contributed files in memory
pars_woIS['OverwriteExisting']=0  # Change this to false, if the files should/can be added in memory
pars_woIS['InitialSplitting']=0
#
#---> Start loop over contributing files
for n in xrange(0,5,1):
     source_file_woIS = 'MER19566_22.0meV_one2one125.nxspe'; # redefine source files list as function of loop number
     target_woIS  = 'MDMAP_T1_woIS'+str(n)+'.nxs';
     # check if the file already been converted to MD and is there
     if not(os.path.exists(target_woIS)):
         print 'Converting ',source_file_woIS
         #current_ws=LoadNXSPE(Filename=source)
         #### For the sample script, simulate load operation above
         current_ws_woIS = CreateSimulationWorkspace(Instrument='MAR',BinParams=[-3,1,3],UnitX='DeltaE',OutputWorkspace=source_file_woIS)
         AddSampleLog(Workspace=current_ws_woIS,LogName='Ei',LogText='3.0',LogType='Number')

         #### Add iformation which is not stored in the nxspe file
         # Add UB matrix (lattice and the beam direction)
         SetUB(Workspace=current_ws_woIS,a='1.4165',b='1.4165',c='1.4165',u='1,0,0',v='0,1,0')
         # Add crystal rotation (assume rotation abgle Psi=5*n where n is file number. Define list of angles if this is not correct
         AddSampleLog(Workspace=current_ws_woIS,LogName='Psi',LogText=str(5*n)+'.',LogType='Number')  # --correct Psi value may be already in nxspe file. This operation is then unnecessary
         # set crystal rotation
         SetGoniometer(Workspace=current_ws_woIS,Axis0='Psi,0,1,0,1')

         # Convert to MD
         pars_woIS['InputWorkspace']=current_ws_woIS;
         md_ws_woIS=ConvertToMD(**pars_woIS)

         # save MD for further usage -- disabled in test script
         #SaveMD(md_ws,Filename=target);
         #DeleteWorkspace(md_ws);  # delete intermediate workspace to save memory
         DeleteWorkspace(current_ws_woIS);

     # add the file name of the file to combine
     if (len(MD_FilesList_woIS) == 0):
         MD_FilesList_woIS = target_woIS;
     else:
         MD_FilesList_woIS=MD_FilesList_woIS+','+target_woIS;



#----------------------------- WITH INITIAL SPLITTING (wIS)-----------------------------------------------------------
# set up target ws name and remove target workspace with the same name which can occasionally exist.
# list of MD files (workspaces) to combine into target MD workspace
MD_FilesList_wIS='';

# define convetr to MD parameters
pars_wIS = dict();
pars_wIS['InputWorkspace']=''
pars_wIS['QDimensions']='Q3D'
pars_wIS['dEAnalysisMode']='Direct'
pars_wIS['Q3DFrames']='HKL'
pars_wIS['QConversionScales']='HKL'
pars_wIS['PreprocDetectorsWS']='preprDetMantid'
pars_wIS['MinValues']='-3,-3,-3.,-50.0'
pars_wIS['MaxValues']='3.,3.,3.,50.0'
pars_wIS['SplitInto']=5
pars_wIS['MaxRecursionDepth']=1
pars_wIS['MinRecursionDepth']=1
pars_wIS['OverwriteExisting']=1  # Change this to false, if the files should/can be added in memory
# test script combines all contributed files in memory
pars_wIS['OverwriteExisting']=0  # Change this to false, if the files should/can be added in memory
pars_wIS['InitialSplitting']=1
#
#---> Start loop over contributing files
for n in xrange(0,5,1):
     source_file_wIS = 'MER19566_22.0meV_one2one125.nxspe'; # redefine source files list as function of loop number
     target_wIS  = 'MDMAP_T1_wIS'+str(n)+'.nxs';
     # check if the file already been converted to MD and is there
     if not(os.path.exists(target_wIS)):
         print 'Converting ',source_file_wIS
         #current_ws=LoadNXSPE(Filename=source)
         #### For the sample script, simulate load operation above
         current_ws_wIS = CreateSimulationWorkspace(Instrument='MAR',BinParams=[-3,1,3],UnitX='DeltaE',OutputWorkspace=source_file_wIS)
         AddSampleLog(Workspace=current_ws_wIS,LogName='Ei',LogText='3.0',LogType='Number')

         #### Add iformation which is not stored in the nxspe file
         # Add UB matrix (lattice and the beam direction)
         SetUB(Workspace=current_ws_wIS,a='1.4165',b='1.4165',c='1.4165',u='1,0,0',v='0,1,0')
         # Add crystal rotation (assume rotation abgle Psi=5*n where n is file number. Define list of angles if this is not correct
         AddSampleLog(Workspace=current_ws_wIS,LogName='Psi',LogText=str(5*n)+'.',LogType='Number')  # --correct Psi value may be already in nxspe file. This operation is then unnecessary
         # set crystal rotation
         SetGoniometer(Workspace=current_ws_wIS,Axis0='Psi,0,1,0,1')

         # Convert to MD
         pars_wIS['InputWorkspace']=current_ws_wIS;
         md_ws_wIS=ConvertToMD(**pars_wIS)

         # save MD for further usage -- disabled in test script
         #SaveMD(md_ws,Filename=target);
         #DeleteWorkspace(md_ws);  # delete intermediate workspace to save memory
         DeleteWorkspace(current_ws_wIS);

     # add the file name of the file to combine
     if (len(MD_FilesList_wIS) == 0):
         MD_FilesList_wIS = target_wIS;
     else:
         MD_FilesList_wIS=MD_FilesList_wIS+','+target_wIS;
