import mantid.simpleapi as api
from mantid.api import *
from mantid.kernel import *

class ScaleWrap(PythonAlgorithm):

    def PyInit(self):
        self.declareProperty(MatrixWorkspaceProperty("InputWorkspace", "", 
                                                     direction=Direction.Input))
        self.declareProperty(MatrixWorkspaceProperty("OutputWorkspace", "", 
                                                     direction = Direction.Output))

    def PyExec(self):
        inputWS = self.getPropertyValue("InputWorkspace")
        outputWS = api.Scale(InputWorkspace=inputWS, Factor=2.0)
        self.setProperty("OutputWorkspace", outputWS)
        
#############################################################################################
registerAlgorithm(ScaleWrap)
