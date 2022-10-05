CreateWorkspace(DataX = [1,1,1], DataY = [1,1,1], OutputWorkspace = 'testWs')
testWs = mtd['testWs']

RenameWorkspace(InputWorkspace= testWs, OutputWorkspace = 'renamed')
rename = mtd['renamed']

print rename.getHistory()
# This works
print rename.getHistory().getAlgorithm(rename.getHistory().size() -2)
#This does not work
print rename.getHistory().getAlgorithm(rename.getHistory().size() -1)