Load('CNCS_7860_event.nxs',OutputWorkspace='CNCS_7860_event')
SetUB(Workspace='CNCS_7860_event',a='10.416499999999999',b='10.416499999999999',c='10.416499999999999',v='0,0,1')
ConvertUnits(InputWorkspace='CNCS_7860_event',OutputWorkspace='CNCS_7860_event',Target='DeltaE',EMode='Direct',EFixed='3')
Rebin(InputWorkspace='CNCS_7860_event',OutputWorkspace='CNCS_7860_event',Params='-3,0.1,3')
CloneWorkspace(InputWorkspace='CNCS_7860_event',OutputWorkspace='preMDpart0')
AddSampleLog(Workspace='preMDpart0',LogName='Psi',LogText='0',LogType='Number Series')
SetGoniometer(Workspace='preMDpart0',Axis0='Psi,0,1,0,1')
ConvertToMDEvents(InputWorkspace='preMDpart0',OutputWorkspace='preMDpart0_md',QDimensions='QhQkQl',MinValues='-1,-1,-1,-1',MaxValues='1,1,1,1',MaxRecursionDepth='1')
#The following works, but these dimension ids do not appear in mantid doc!
SliceMD(InputWorkspace='preMDpart0_md',AlignedDimX='Q1, -1, 1, 10',AlignedDimY='Q2, -1, 1, 10',AlignedDimZ='Q3, -1, 1, 10',AlignedDimT='DeltaE,-1,1,1',OutputWorkspace='t')