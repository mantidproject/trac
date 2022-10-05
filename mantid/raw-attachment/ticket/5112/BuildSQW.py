print 'start\n'
cur_ws='wsn';
md_ws='mdws4D';
MDWSF='';
print 'for\n'
for n in range(15052,15179):
	print 'Load\n'	
#    LoadNXSPE(Filename='D:/Data/Fe/Fe_Mantid/MAP'+str(n)+'.nxspe',OutputWorkspace=cur_ws)
	print 'SetUB\n'		
#	SetUB(Workspace=cur_ws,a='2.87',b='2.87',c='2.87')
#	ConvertToMDEvents(InputWorkspace=cur_ws,OutputWorkspace=md_ws,QDimensions='Q3D',UsePreprocessedDetectors='1',MinValues='-4.2,-4.2,-4.2,-50',MaxValues='4.2,4.2,4.2,350',SplitInto='50',MaxRecursionDepth='1',MinRecursionDepth='1')
#	SaveMD(md_ws,'MDMAP'+str(n)+'.nxs');
#	DeleteWorkspace(md_ws);
#	DeleteWorkspace(cur_ws);	
	MDWSF=MDWSF+'MDMAP'+str(n)+'.nxs;';

# Correct syntaxis: MergeMDFiles(MDWSF,OutputFilename='fe400_8k.nxs',Parallel='1');
# Wrons syntaxis:
MergeMDFiles(MDWSF,'ws2',OutputFilename='fe400_8k.nxs',Parallel='1',OutputFilename='fe400_8k.nxs');