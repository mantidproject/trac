# Test MergeReplaceExisting 
ws1 = CreateWorkspace(OutputWorkspace='SomeWorkspace',DataX='1',DataY='2',DataE='3',UnitX='Label',VerticalAxisUnit='Empty',VerticalAxisValues='0')
ws2 = CreateWorkspace(OutputWorkspace='SomeOtherWorkspace',DataX='1',DataY='2',DataE='3',UnitX='Label',VerticalAxisUnit='Empty',VerticalAxisValues='0')

#Add logs to first workspace
AddSampleLog(Workspace='SomeWorkspace',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeWorkspace',LogName='B',LogText='World')
AddSampleLog(Workspace='SomeWorkspace',LogName='D',LogText='Yeah!')

#Add logs to second workspace
AddSampleLog(Workspace='SomeOtherWorkspace',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeOtherWorkspace',LogName='B',LogText='Universe')
AddSampleLog(Workspace='SomeOtherWorkspace',LogName='C',LogText='Today')

CopyLogs(InputWorkspace=ws1, OutputWorkspace=ws2,MergeStrategy="MergeReplaceExisting")


# Test WipeExisting
ws4 = CreateWorkspace(OutputWorkspace='SomeOtherWorkspace2',DataX='1',DataY='2',DataE='3',UnitX='Label',VerticalAxisUnit='Empty',VerticalAxisValues='0')

#Add logs to first workspace
AddSampleLog(Workspace='SomeWorkspace',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeWorkspace',LogName='B',LogText='World')
AddSampleLog(Workspace='SomeWorkspace',LogName='D',LogText='Yeah!')

#Add logs to second workspace
AddSampleLog(Workspace='SomeOtherWorkspace2',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeOtherWorkspace2',LogName='B',LogText='Universe')
AddSampleLog(Workspace='SomeOtherWorkspace2',LogName='C',LogText='Today')

CopyLogs(InputWorkspace=ws1, OutputWorkspace=ws4,MergeStrategy="WipeExisting")


# Test MergeKeepExisting
ws6 = CreateWorkspace(OutputWorkspace='SomeOtherWorkspace3',DataX='1',DataY='2',DataE='3',UnitX='Label',VerticalAxisUnit='Empty',VerticalAxisValues='0')

#Add logs to first workspace
AddSampleLog(Workspace='SomeWorkspace',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeWorkspace',LogName='B',LogText='World')
AddSampleLog(Workspace='SomeWorkspace',LogName='D',LogText='Yeah!')

#Add logs to second workspace
AddSampleLog(Workspace='SomeOtherWorkspace3',LogName='A',LogText='Hello')
AddSampleLog(Workspace='SomeOtherWorkspace3',LogName='B',LogText='Universe')
AddSampleLog(Workspace='SomeOtherWorkspace3',LogName='C',LogText='Today')

CopyLogs(InputWorkspace=ws1, OutputWorkspace=ws6,MergeStrategy="MergeKeepExisting")