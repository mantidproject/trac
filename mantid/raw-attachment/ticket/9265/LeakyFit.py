import math
import numpy
from mantid.api import * # PythonAlgorithm, registerAlgorithm, WorkspaceProperty
from mantid.kernel import *
from mantid.simpleapi import *

class LeakyFunction(IFunction1D):
	# equivalent to ExpDecayOsc
	def init(self):
		self.declareParameter("A",1.0)
		self.declareParameter("Lambda",1.0)
		self.declareParameter("Frequency",1.0)
		self.declareParameter("Phi",1.0)

	def function1D(self,xvals):
		a=self.getParameterValue("A")
		lam=self.getParameterValue("Lambda")
		frq=self.getParameterValue("Frequency")
		phi=self.getParameterValue("Phi")
		return a*numpy.cos(xvals*frq*2.0*math.pi+phi)*numpy.exp(-xvals*lam)

FunctionFactory.subscribe(LeakyFunction)

class LeakyFit(PythonAlgorithm):
	def PyInit(self):
		#self.declareProperty(WorkspaceProperty("InputWS","",Direction.Input),"Source run")
		#self.declareProperty(WorkspaceProperty("InputWS","",Direction.Input),"Data to fit, from CreateALCMap")
		self.declareProperty(WorkspaceProperty("OutputWSChi","",Direction.Output),"Chisq as a function of fixed F")
		self.declareProperty(WorkspaceProperty("OutputWSA","",Direction.Output),"Signal ampl as a function of fixed F")
		#self.declareProperty("StartF",0.0,doc="Lowest val of F")
		#self.declareProperty("EndF",0.5,doc="Highest val of F")
		#self.declareProperty("FPoints",20,doc="Number of F values to try")
		self.declareProperty("UsePythonFunc",True,doc="Use Python function instead of built in C++ one")

	def category(self):
		return "Muon"
		
	def PyExec(self):
		#sourcedat=self.getProperty("InputWS").value
		#(flatsource,Nspec,Y0,dY,dX)=QuantumFlattenWorkspace(InputWorkspace=sourcedat)
		sourcedat=WorkspaceFactory.create("Workspace2D",NVectors=1,XLength=5000,YLength=5000)
		sourcedat.dataX(0)[:]=numpy.linspace(0.0,32.0,5000)
		sourcedat.dataY(0)[:]=10.0*numpy.cos(sourcedat.dataX(0))+0.1*numpy.random.randn(5000)
		sourcedat.dataE(0)[:]=numpy.ones(5000)*0.1
		# Y0=field val of 1st spectrum, dY=field increment, dX=X value offset between spectra

		#StartF=self.getProperty("StartF").value
		#EndF=self.getProperty("EndF").value
		#FPoints=self.getProperty("FPoints").value
		StartF=0.1
		EndF=0.5
		FPoints=20
		usePythonFunc=self.getProperty("UsePythonFunc").value
		resultws=WorkspaceFactory.create("Workspace2D",NVectors=1,XLength=FPoints,YLength=FPoints)
		amplws=WorkspaceFactory.create("Workspace2D",NVectors=1,XLength=FPoints,YLength=FPoints)
		# progress
		prog_reporter=Progress(self,start=0.0, end=1.0, nreports=FPoints)
		FVals=numpy.linspace(StartF,EndF,FPoints)
		resultws.dataX(0)[:]=FVals
		amplws.dataX(0)[:]=FVals
		
		for j in range(FPoints):
			F=FVals[j]
			if(usePythonFunc):
				(stat,chisq,Covar,params,curves)=Fit(Function="name=LeakyFunction,A=0.2,Lambda=0.05,Frequency="+str(F)+",Phi=0.0",
					ties="Frequency="+str(F),InputWorkspace=sourcedat,Output="sourcedat")
			else:
				(stat,chisq,Covar,params,curves)=Fit(Function="name=ExpDecayOsc,A=0.2,Lambda=0.05,Frequency="+str(F)+",Phi=0.0",
					ties="Frequency="+str(F),InputWorkspace=sourcedat,Output="sourcedat")
			resultws.dataY(0)[j]=chisq
			amplws.dataY(0)[j]=params.column(1)[0]
			DeleteWorkspace(Covar)
			DeleteWorkspace(params)
			DeleteWorkspace(curves)

			prog_reporter.report("Processing")
		self.setProperty("OutputWSChi",resultws)
		self.setProperty("OutputWSA",amplws)

AlgorithmFactory.subscribe(LeakyFit)
