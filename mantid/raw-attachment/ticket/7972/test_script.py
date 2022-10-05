ws1 = CreateWorkspace(OutputWorkspace='SomeWorkspace',DataX='1',DataY='2',DataE='3',UnitX='Label',VerticalAxisUnit='Empty',VerticalAxisValues='0')
ws2 = CreateWorkspace(OutputWorkspace='SomeOtherWorkspace',DataX='1',DataY='2',DataE='3',UnitX='Label',VerticalAxisUnit='Empty',VerticalAxisValues='0')

#Add logs to first workspace
AddSampleLog(Workspace='SomeWorkspace',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeWorkspace',LogName='B',LogText='World')

#Add logs to second workspace
AddSampleLog(Workspace='SomeOtherWorkspace',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeOtherWorkspace',LogName='B',LogText='Universe')

CopyLogs(InputWorkspace=ws1, OutputWorkspace=ws2,MergeStrategy="MergeReplaceExisting")
