# Algorithm to start Jump fit programs
from mantid.api import PythonAlgorithm, AlgorithmFactory
from mantid.kernel import StringListValidator, StringMandatoryValidator
from mantid.simpleapi import *
from mantid import config, logger, mtd
import os.path
from IndirectBayes import JumpRun

class JumpFit(PythonAlgorithm):
 
	def category(self):
		return "Workflow\\MIDAS;PythonAlgorithms"

	def PyInit(self):
		self.declareProperty(name='InputType',defaultValue='File',validator=StringListValidator(['File','Workspace']), doc='Origin of data input - File (*.nxs) or Workspace')
		self.declareProperty(name='Instrument',defaultValue='iris',validator=StringListValidator(['irs','iris','osi','osiris']), doc='Instrument')
		self.declareProperty(name='Analyser',defaultValue='graphite002',validator=StringListValidator(['graphite002','graphite004']), doc='Analyser & reflection')
		self.declareProperty(name='QLprogram',defaultValue='QLr',validator=StringListValidator(['QLr','QLd']), doc='QL output from Res or Data')
		self.declareProperty(name='Fit',defaultValue='CE',validator=StringListValidator(['CE','SS']), doc='Chudley-Elliott or Singwi-Sjolander')
		self.declareProperty(name='Width',defaultValue='width11',validator=StringListValidator(['width11','width21','width22']), doc='FullWidth type')
		self.declareProperty(name='SamNumber',defaultValue='',validator=StringMandatoryValidator(), doc='Sample run number')
		self.declareProperty(name='CropQ',defaultValue=False, doc='Switch CropQ Off/On')
		self.declareProperty(name='Qmin',defaultValue='', doc='Qmin for cropping')
		self.declareProperty(name='Qmax',defaultValue='', doc='Qmax for cropping')
		self.declareProperty(name='Plot',defaultValue=False, doc='Switch Plot Off/On')
		self.declareProperty(name='Verbose',defaultValue=True, doc='Switch Verbose Off/On')
		self.declareProperty(name='Save',defaultValue=False, doc='Switch Save result to nxs file Off/On')
 
	def PyExec(self):
		
		self.log().information('Jump input')
		inType = self.getPropertyValue('InputType')
		prefix = self.getPropertyValue('Instrument')
		ana = self.getPropertyValue('Analyser')
		prog = self.getPropertyValue('QLprogram')
		jump = self.getPropertyValue('Fit')
		width = self.getPropertyValue('Width')
		if width == 'width11':
			index = 0
		if width == 'width21':
			index = 2
		if width == 'width22':
			index = 4
		sam = self.getPropertyValue('SamNumber')

		samWS = prefix+sam+'_'+ana+'_'+prog
		cropOp = self.getProperty('CropQ').value
		verbOp = self.getProperty('Verbose').value
		plotOp = self.getProperty('Plot').value
		saveOp = self.getProperty('Save').value

		workdir = config['defaultsave.directory']
		if inType == 'File':
			path = os.path.join(workdir, samWS+'_Workspace.nxs')					# path name for nxs file
			LoadNexusProcessed(Filename=path, OutputWorkspace=samWS)
			message = 'Input from File : '+path
		else:
			message = 'Input from Workspace : '+samWS
		ExtractSingleSpectrum(InputWorkspace=samWS, OutputWorkspace=samWS, WorkspaceIndex=index)		
		inGR = mtd[samWS].getRun()
		val = inGR.getLogData('Fit Program').value
		if verbOp:
			logger.notice(message)
			logger.notice('Fit program was : '+val)
		x = mtd[samWS].readX(0)
		xmin = x[0]
		xmax = x[len(x)-1]
		if cropOp:
			Crop = False
			qmin = self.getPropertyValue('Qmin')
			qmin = float(qmin)
			qmax = self.getPropertyValue('Qmax')
			qmax = float(qmax)
			if qmin > xmin:
				Crop = True
			if qmax < xmax:
				Crop = True
			if Crop:
				CropWorkspace(InputWorkspace=samWS, OutputWorkspace=samWS,
					XMin=qmin, XMax=qmax)
				if verbOp:
					logger.notice('Cropping from Q= ' + str(qmin) +' to '+ str(qmax))
		JumpRun(samWS,jump,verbOp,plotOp,saveOp)

AlgorithmFactory.subscribe(JumpFit)         # Register algorithm with Mantid
