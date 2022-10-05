Load(Filename='CNCS_7860_event.nxs',OutputWorkspace='CNCS_7860_event')
ConvertUnits(InputWorkspace='CNCS_7860_event',OutputWorkspace='CNCS_7860_event',Target='DeltaE',EMode='Direct',EFixed='3')
Rebin(InputWorkspace='CNCS_7860_event',OutputWorkspace='CNCS_7860_event',Params='-1,0.05,3',PreserveEvents=False)
SetUB(Workspace='CNCS_7860_event',a='3',b='4',c='5',u='0,1,0',v='1,0,0')

for i in range(0,20,5):
    CloneWorkspace(InputWorkspace='CNCS_7860_event',OutputWorkspace='preMDpart'+str(i))
    AddSampleLog(Workspace='preMDpart'+str(i),LogName='Psi',LogText='0',LogType='Number Series')
    SetGoniometer(Workspace='preMDpart'+str(i),Axis0='Psi,0,1,0,1')