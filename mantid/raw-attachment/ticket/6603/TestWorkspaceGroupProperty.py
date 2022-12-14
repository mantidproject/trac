"""*WIKI* 
*WIKI*"""


from mantid.kernel import *
from mantid.api import *
import numpy as np

import os

class TestWorkspaceGroupProperty(PythonAlgorithm):
    """
    """
   
    def category(self):
        return "PythonAlgorithms"

    def name(self):
        return "WorkspaceGroupProperty"

    def PyInit(self):
        self.declareProperty(WorkspaceGroupProperty("InputWorkspace", "", Direction.Input), doc="Group workspace that automatically includes all members.")
        self.declareProperty(MatrixWorkspaceProperty("InputWorkspace2", "", Direction.Input), doc="asd")
   
    def PyExec(self):
        ws = self.getProperty("InputWorkspace").value
        logger.notice("Input type: %s" % str(type(ws)))
        ws2 = self.getProperty("InputWorkspace2").value
        logger.notice("Input type: %s" % str(type(ws2)))
        
        
registerAlgorithm(TestWorkspaceGroupProperty)
