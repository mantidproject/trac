"""*WIKI* 

<math>~20%</math>
<math>T^' = 0.158</math>

*WIKI*"""


from mantid.kernel import *
from mantid.api import PythonAlgorithm, AlgorithmFactory

class Dummy(PythonAlgorithm):
  def PyInit(self):
    #self.declareProperty(MatrixWorkspaceProperty("LHSWorkspace", "", Direction.Input), "Input workspace")
    pass
  def PyExec(self):
    # Run the algorithm
    pass
# Register algorithm with Mantid
AlgorithmFactory.subscribe(Dummy)
