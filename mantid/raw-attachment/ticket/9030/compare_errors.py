test_num = 1
testnames =['EQSANSTransmissionDC',
'EQSANSTransmissionEvent',
'EQSANSTransmission',
'JumpCETest',
'JumpFickTest',
'JumpSSTest',
'LOQCentreNoGravDefineCentre',
'LOQCentreNoGrav',
'LOQMinimalBatchReduction',
'LOQReductionOnLoadedWorkspaceMustProduceTheSameResult_1',
'LOQReductionOnLoadedWorkspaceMustProduceTheSameResult_2',
'LOQTransFitWorkspace2D',
'LOQTransFitWorkspace2DWithLoadedWorkspace',
'SANS2DWaveloops',
'SANS2DWaveloopsReloadWorkspace',
'SANSLOQBatch',
'VesuvioFittingTest',
'VesuvioFittingWithKFreeTest',
'VesuvioFittingWithQuadraticBackgroundTest'
]
print len(testnames)
testname = testnames[test_num]
print testname
original_name = testname
current_name = testname+'-mismatch'


new_matches = {'SANS2DWaveloopsReloadWorkspace':'SANS2DWaveloops.nxs',
'LOQTransFitWorkspace2DWithLoadedWorkspace':'LOQTransFitWorkspace2D.nxs',
'LOQReductionOnLoadedWorkspaceMustProduceTheSameResult_2':'LOQCentreNoGrav.nxs',
'LOQCentreNoGravDefineCentre': 'LOQCentreNoGrav.nxs',
'LOQReductionOnLoadedWorkspaceMustProduceTheSameResult_1':'LOQCentreNoGravSearchCentreFixed.nxs',
'LOQMinimalBatchReduction':'LOQReductionMergedData.nxs',
'JumpSSTest':'ISISIndirectBayes_JumpSSTest.nxs', 
'JumpCETest':'ISISIndirectBayes_JumpCETest.nxs', 
'JumpFickTest':'ISISIndirectBayes_JumpFickTest.nxs', 
'EQSANSTransmission':'EQSANSTrans.nxs',
'EQSANSTransmissionEvent':'EQSANSTransEvent.nxs'
}

for k,v in new_matches.items():
	if testname == k: original_name = v


mtd.clear()

ws1 = Load(original_name)
ws2 =  Load(current_name)



def compareErrors(ws1, ws2, index):
  axisX = range(len(ws1.readE(index)))
  original = CreateWorkspace(axisX, ws1.readE(index), OutputWorkspace='original'+str(index))
  new_err = CreateWorkspace(axisX, ws2.readE(index), OutputWorkspace='new_err'+str(index))
  a = plotSpectrum(original, 0)
  plotSpectrum(new_err, 0, window=a)
  b = plotSpectrum(ws1, index, True)
  plotSpectrum(ws2, index, True, window=b)


for i in range(ws1.getNumberHistograms()):
	compareErrors(ws1, ws2, i)

