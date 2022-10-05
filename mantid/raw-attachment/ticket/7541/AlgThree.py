
import mantid.simpleapi as api

from mantid.api import *
from mantid.kernel import *

class AlgThree(PythonAlgorithm):

    def category(self):
        return "PythonAlgorithms"

    def name(self):
	    return "AlgThree"

    def PyInit(self):
        self.declareProperty(MatrixWorkspaceProperty("WorkspaceA", "", Direction.Input), "Input workspace")
        self.declareProperty(MatrixWorkspaceProperty("OutputWorkspace", "", Direction.Output), "Output Workspace")
 
    def PyExec(self):
        pass
        

#############################################################################################

AlgorithmFactory.subscribe(AlgThree())
