"""*WIKI* 

Calculates the scattering & transmission for Indirect Geometry spectrometers. The sample chemical formula is input for the SetSampleMaterial algorithm to calculate the cross-sections.
The instrument analyser reflection is selected to obtain the wavelength to calculate the absorption cross-section. The sample number density & thickness is input to then calculate the percentage scattering & transmission.

*WIKI*"""

from mantid.simpleapi import *
from mantid.api import PythonAlgorithm, AlgorithmFactory
from mantid.kernel import StringListValidator, StringMandatoryValidator
from mantid import config
from IndirectCommon import StartTime, EndTime
import os.path, math

class IndirectTransmission(PythonAlgorithm):
 
	def category(self):
		return "Workflow\\MIDAS;PythonAlgorithms"

	def PyInit(self):
		self.declareProperty(name='Instrument',defaultValue='IRIS',validator=StringListValidator(['IRIS','OSIRIS']), doc='Instrument')
		self.declareProperty(name='Analyser',defaultValue='graphite',validator=StringListValidator(['graphite','fmica']), doc='Analyser')
		self.declareProperty(name='Reflection',defaultValue='002',validator=StringListValidator(['002','004']), doc='Reflection')
		self.declareProperty(name='Chemical Formula',defaultValue='',validator=StringMandatoryValidator(), doc='Sample chemical formula')
		self.declareProperty(name='Number Density', defaultValue=0.1, doc='Number denisty. Default=0.1')
		self.declareProperty(name='Thickness', defaultValue=0.1, doc='Sample thickness. Default=0.1')
 
	def PyExec(self):

		StartTime('IndirectTransmission')
		
		instrumentName = self.getPropertyValue('Instrument')
		analyser = self.getPropertyValue('Analyser')
		reflection = self.getPropertyValue('Reflection')
		formula = self.getPropertyValue('Chemical Formula')
		density = self.getPropertyValue('Number Density')
		thickness = self.getPropertyValue('Thickness')
		
		#Load instrument defintion file
		idfDir = config['instrumentDefinition.directory']
		idf = idfDir + instrumentName + '_Definition.xml'
		workspace = '__empty_'+instrumentName
		LoadEmptyInstrument(OutputWorkspace=workspace, Filename=idf)

		#Load instrument parameter file
		nameStem = instrumentName + '_' + analyser + '_' + reflection
		ipf = idfDir + nameStem + '_Parameters.xml'
		LoadParameterFile(Workspace=workspace, Filename=ipf)

		#Get efixed value
		instrument = mtd[workspace].getInstrument()
		efixed = instrument.getNumberParameter('efixed-val')[0]

		logger.notice('Analyser : ' +analyser+reflection +' with energy = ' + str(efixed))

		result = SetSampleMaterial(InputWorkspace=workspace,ChemicalFormula=formula)

		#elastic wavelength
		wave=1.8*math.sqrt(25.2429/efixed)

		absorptionXSection = result[5]*wave/1.7982
		coherentXSection = result[4]
		incoherentXSection = result[3]
		scatteringXSection = result[3]

		thickness = float(thickness)
		density = float(density)

		totalXSection = absorptionXSection + scatteringXSection

		transmission = math.exp(-density*totalXSection*thickness)
		scattering = 1.0 - math.exp(-density*scatteringXSection*thickness)
		
		#Create table workspace to store calculations
		tableWs = nameStem + '_Transmission'
		tableWs = CreateEmptyTableWorkspace(OutputWorkspace=tableWs)
		tableWs.addColumn("str", "Name")
		tableWs.addColumn("str", "Value")

		#Add values to table workspace
		tableWs.addRow(['Absorption Xsection at wavelength ', str(wave) +
			' A = '+str(absorptionXSection)])
		tableWs.addRow(['Coherent Xsection', str(coherentXSection)])
		tableWs.addRow(['Incoherent Xsection', str(incoherentXSection)])
		tableWs.addRow(['Total scattering Xsection', str(scatteringXSection)])
		tableWs.addRow(['Number density', str(density)])
		tableWs.addRow(['Thickness', str(thickness)])
		tableWs.addRow(['Transmission (abs+scatt)', str(transmission)])
		tableWs.addRow(['Total scattering', str(scattering)])

		#Output values to the results log
		logger.notice('Absorption Xsection at wavelength ' + str(wave) +
			' A = '+str(absorptionXSection))
		logger.notice('Coherent Xsection = '+ str(coherentXSection))
		logger.notice('Incoherent Xsection = ' + str(incoherentXSection))
		logger.notice('Total scattering Xsection = ' + str(scatteringXSection))
		logger.notice('Number density = ' + str(density))
		logger.notice('Thickness = ' + str(thickness))
		logger.notice('Transmission (abs+scatt) = ' +str(transmission))
		logger.notice('Total scattering = ' +str(scattering))

		#remove idf/ipf workspace
		DeleteWorkspace(workspace)

		EndTime('IndirectTransmission')

# Register algorithm with Mantid
AlgorithmFactory.subscribe(IndirectTransmission)
