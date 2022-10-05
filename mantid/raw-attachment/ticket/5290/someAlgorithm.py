class SomeAlgorithm(PythonAlgorithm):
	def PyInit(self):
		# Declare algorithm properties.
		self.declareProperty('Input', '' , MandatoryValidator(), Description='')

	def PyExec(self):
		print self.getPropertyValue("Input")

# Register algorthm with Mantid.
mantid.registerPyAlgorithm(SomeAlgorithm())