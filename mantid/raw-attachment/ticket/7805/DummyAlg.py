# Algorithm to start Force
from mantid.api import PythonAlgorithm, AlgorithmFactory
from mantid.kernel import FloatBoundedValidator, IntBoundedValidator

class BoundedValidatorTestAlg(PythonAlgorithm):
 
	def category(self):
		return "PythonAlgorithms"

	def PyInit(self):
		self.declareProperty(name='FloatValue',defaultValue=5.0,validator=FloatBoundedValidator(1.0,10.0,True), doc='A Float Value')
		self.declareProperty(name='IntValue',defaultValue=2,validator=IntBoundedValidator(1,5,True), doc='An Int Value')

	def PyExec(self):
		print "This is a dummy algorithm! Did you expecting it to do something?"

AlgorithmFactory.subscribe(BoundedValidatorTestAlg) # Register algorithm with Mantid
