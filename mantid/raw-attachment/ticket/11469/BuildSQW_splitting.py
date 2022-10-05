###########################################################################
##   Sample script to build Mantid's combined MD workspace               ##
##    equivalent  of Horace sqw  object                                  ##
###########################################################################
data_path=os.path.dirname(os.path.realpath(__file__))
config.appendDataSearchDir(data_path)

config['defaultsave.directory']=data_path
save_dir = config.getString('defaultsave.directory')
print "Data will be saved into: ",save_dir

#
print 'Start converting \n'
# 
preprocessedDetectorsWSName='preprDetMAPS'
# List of the comma-separated file names to merge
MDWS_FilesList='';

#efix=34.96;

# ConvertToMD parameters defined out of the loop
pars = dict();
pars['InputWorkspace']=''
pars['QDimensions']='Q3D'
pars['dEAnalysisMode']='Direct'
pars['Q3DFrames']='HKL'
pars['QConversionScales']='HKL'
pars['PreprocDetectorsWS']=preprocessedDetectorsWSName;
pars['MinValues']='-3,-3,-3,-2'
pars['MaxValues']='3,3,3,23'
pars['SplitInto']='50,50,50,60'
pars['OverwriteExisting']=False
# Currently works only with  1
pars['MaxRecursionDepth']=1
pars['MinRecursionDepth']=1
pars['TopLevelSplitting']=1

nFiles = 2
print " processing {0} spe files".format(nFiles)

for n in xrange(0,nFiles):
    source = 'MAP0'+str(5935+n)+'_4to1_033.nxspe';
    target  = 'MDMAP'+str(5935+n)+'_4to1_033.nxs';
    #while not(os.path.exists(save_dir+source)):

    if not(os.path.exists(save_dir+target)):
        print 'Converting ',source
        cur_ws=LoadNXSPE(Filename=source)

        # save disk space, remove source file
        # (it should  be stored somewhere) in archive
        #os.remove(source);

        # Add incident energy log.  May be not necessary for NXSPE or nxs files
        #AddSampleLog(Workspace=cur_ws,LogName='Ei',LogText=str(efix),LogType='Number')
        # Add rotation angle log.  May be not necessary for NXSPE or nxs files
        #AddSampleLog(Workspace=cur_ws,LogName='Psi',LogText=str(psi[n])+'.',LogType='Number')

        # Set projection matrix
        SetUB(Workspace=cur_ws,a=4.2275,b=4.2275,c=4.2275,u='1,1,0',v='0,0,1')
        # rotated by proper number of degrees around rotation axis, which in usual Horace set-up is parallel to  second projection axis
        SetGoniometer(Workspace=cur_ws,Axis0='Psi,0,1,0,1')
        print "Goniometer angles: ",cur_ws.getRun().getGoniometer().getEulerAngles('XYZ')


        # set up source workspace
        pars['InputWorkspace']=cur_ws;
	# Convert To MD
        target_MDws=ConvertToMD(**pars)

        # Save data for future usage
        SaveMD(target_MDws,Filename=target );
	# Clear memory 
        DeleteWorkspace(target_MDws);
        DeleteWorkspace(cur_ws);

    if (len(MDWS_FilesList) == 0):
        MDWS_FilesList = target;
    else:
        MDWS_FilesList=MDWS_FilesList+','+target;


ws4D = MergeMDFiles(MDWS_FilesList,OutputFilename='RbMnF3_test.nxs', Parallel='0');

######################################################################


