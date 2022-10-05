
import mantid.simpleapi as api

from mantid.api import *
from mantid.kernel import *

class AlgTwo(PythonAlgorithm):

    def category(self):
        return "PythonAlgorithms"

    def name(self):
	    return "AlgTwo"

    def PyInit(self):
        self.declareProperty(MatrixWorkspaceProperty("WorkspaceA", "", Direction.Input), "Input workspace")
        self.declareProperty(MatrixWorkspaceProperty("WorkspaceB", "", Direction.Input), "Input workspace")
        self.declareProperty(MatrixWorkspaceProperty("InputWorkspace", "", Direction.Input), "Input workspace")
        self.declareProperty(MatrixWorkspaceProperty("WorkspaceC", "", Direction.Input), "Input workspace")
        self.declareProperty(MatrixWorkspaceProperty("OutputWorkspace", "", Direction.Output), "Output Workspace")
 
    def PyExec(self):
        pass
        

#############################################################################################

AlgorithmFactory.subscribe(AlgTwo())
