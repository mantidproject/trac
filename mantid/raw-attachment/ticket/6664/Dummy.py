from mantid.kernel import *
from mantid.api import *
 
class Dummy(PythonAlgorithm):
	
	def PyInit(self):
		#self.declareProperty(MatrixWorkspaceProperty("LHSWorkspace", "", Direction.Input), "Input workspace")
		pass

	def PyExec(self):
		# Run the algorithm
		pass
 
# Register algorithm with Mantid
registerAlgorithm(Dummy)
