WS_Name = 'CNCS_7860_event'

#WS_Name = 'MAR11001'
Load(Filename='CNCS_7860_event.nxs',OutputWorkspace=WS_Name )
ConvertUnits(InputWorkspace=WS_Name,OutputWorkspace=WS_Name,Target='DeltaE',EMode='Direct',EFixed='3')
Rebin(InputWorkspace='CNCS_7860_event',OutputWorkspace=WS_Name,Params='-1,0.05,3',PreserveEvents=False)
SetUB(Workspace=WS_Name,a='1.4165',b='1.4165',c='1.4165',u='1,0,0',v='0,1,0')
#AddSampleLog(Workspace=WS_Name,LogName='Ei',LogText='3',LogType='Number')
#AddSampleLog(Workspace=WS_Name,LogName='Psi',LogText='0',LogType='Number Series')
#SetGoniometer(Workspace=WS_Name,Axis0='Psi,1,0,0,1')


#for i in range(0,20,1):
TWS='MD3'
saveDir='/home/rff93/testing/4480/'
for i in range(0,20,5):
    
  CloneWorkspace(InputWorkspace=WS_Name,OutputWorkspace='preMDpart'+str(i))
    
  AddSampleLog(Workspace='preMDpart'+str(i),LogName='Psi',LogText=str(i),LogType='Number Series')
  SetGoniometer(Workspace='preMDpart'+str(i),Axis0='Psi,0,1,0,1')
  SaveNXSPE(InputWorkspace='preMDpart'+str(i),Filename=saveDir+str(i)+'.nxspe',Efixed=3,Psi=i)
    
  ConvertToMDEvents(InputWorkspace='preMDpart'+str(i),OutputWorkspace='MDpart'+str(i),QDimensions='QhQkQl',u='1,0,0',v='0,1,0',dEAnalysisMode='Direct',MinValues='-2,-2,-3,-1',MaxValues='2,2,3,3',SplitInto="20,20,1,1")
#ConvertToMDEvents(InputWorkspace=WS_Name,OutputWorkspace=TWS,QDimensions='QhQkQl',u='0,1,0',v='0,0,1',dEAnalysisMode='Direct',MinValues='-2,-2,-3,-1',MaxValues='2,2,3,3',SplitInto="20,20,1,1")
PlusMD(LHSWorkspace='MDpart0',RHSWorkspace='MDpart5',OutputWorkspace=TWS)
PlusMD(LHSWorkspace=TWS,RHSWorkspace='MDpart10',OutputWorkspace=TWS)
PlusMD(LHSWorkspace=TWS,RHSWorkspace='MDpart15',OutputWorkspace=TWS)
plotSlice(TWS, xydim=["Q1","Q2"], slicepoint=[0,0] )


