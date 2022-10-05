from MantidFramework import *

def RunFFT(InputWorkspace, OutputWorkspace, Real):
	algm = mantid.createAlgorithm("FFT")
	algm.setPropertyValue("InputWorkspace", makeString(InputWorkspace).lstrip('? '))
	algm.setPropertyValue("OutputWorkspace", makeString(OutputWorkspace).lstrip('? '))
	algm.setPropertyValue("Real", makeString(Real).lstrip('? '))
	algm.execute()

class FuryCompile(PythonAlgorithm):
	
	def PyInit(self):
		self.declareWorkspaceProperty("InputWorkspace", "", Direction.Input)
		self.declareWorkspaceProperty("OutputWorkspace", "", Direction.Output)
		self.declareProperty("FFTPart", 2)
		
	def PyExec(self):
		inWS = self.getProperty("InputWorkspace")
		fftPart = self.getProperty("FFTPart")
		nhist = inWS.getNumberHistograms()
		
		for i in range(0, nhist):
			tmpWS = '_fury_algorithm_temp'
			RunFFT(inWS, tmpWS, i)
			
			tempWS = mantid.getMatrixWorkspace(tmpWS)
			#tempWS = WorkspaceFactory.createMatrixWorkspace(3,inWS.getNumberBins(), inWS.getNumberBins())
			if ( i == 0 ):
				outWS = WorkspaceFactory.createMatrixWorkspaceFromCopy(tempWS, nhist, tempWS.getNumberBins(), tempWS.getNumberBins())
			
			for j in range(0, outWS.getNumberBins()):
				outWS.dataX(i)[j] = tempWS.readX(fftPart)[j]
				outWS.dataE(i)[j] = tempWS.readE(fftPart)[j]
				outWS.dataY(i)[j] = tempWS.readY(fftPart)[j]
				
		self.setProperty("OutputWorkspace", outWS)

mantid.registerPyAlgorithm(FuryCompile())
