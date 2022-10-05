trans = Load('INTER00013463.nxs')
CreateTransmissionWorkspaceAuto(trans, OutputWorkspace='Test')
DeleteWorkspace(trans)
def printHistory(algHist, depth=1):
	for child in algHist.getChildHistories():
		print ''.join('>'*depth) + child.name()
		printHistory(child, depth+1)

t = mtd["Test"]
h=t.getHistory()
l=h.getAlgorithmHistories()
for child in l:
	print child.name()
	printHistory(child)
