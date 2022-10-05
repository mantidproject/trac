workspace_name = 'MAR11001';
#workspace_name = 'MARI11001';
Load(Filename='MAR11001.RAW',OutputWorkspace=workspace_name)
#ConvertUnits(InputWorkspace='MARI11001',OutputWorkspace='',Target='DeltaE',EMode='Direct',EFixed='3')
AddSampleLog(Workspace=workspace_name,LogName='phi',LogText='0',LogType='Number Series')
AddSampleLog(Workspace=workspace_name,LogName='chi',LogText='0',LogType='Number Series')
AddSampleLog(Workspace=workspace_name,LogName='omega',LogText='10',LogType='Number Series')

GetEi(InputWorkspace=workspace_name,Monitor1Spec='2',Monitor2Spec='3',EnergyEstimate='13')
#Rebin(InputWorkspace='MARI11001',OutputWorkspace='s1',Params='-2.9,0.05,2.9',PreserveEvents='0')
try:
    #ConvertToMDEvents(InputWorkspace=workspace_name,OutputWorkspace='ss',UsePreprocessedDetectors='1',QDimensions="QxQyQz",OtherDimensions='',dEAnalysisMode="Direct",MinValues='-10,-10,-10,-2',MaxValues='10,10,10,10')
    CloneWorkspace(InputWorkspace='MAR11001',OutputWorkspace='MAR11002')
    CloneWorkspace(InputWorkspace='MAR11001',OutputWorkspace='MAR11003')
except e:
    mtd.sendErrorMessage(e)
