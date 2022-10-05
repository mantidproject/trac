
import mantid.simpleapi as api

from mantid.api import *
from mantid.kernel import *

class AlgOne(PythonAlgorithm):

    def category(self):
        return "PythonAlgorithms"

    def name(self):
	    return "AlgOne"

    def PyInit(self):
        self.declareProperty(MatrixWorkspaceProperty("InputWorkspace", "", Direction.Input), "Input workspace")
        self.declareProperty(MatrixWorkspaceProperty("OutputWorkspace", "", Direction.Output), "Output Workspace")
 
    def PyExec(self):
        pass
        

#############################################################################################

AlgorithmFactory.subscribe(AlgOne())
