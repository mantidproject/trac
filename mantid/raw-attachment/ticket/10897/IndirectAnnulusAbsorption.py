# Algorithm to start Decon
from mantid.simpleapi import *
from mantid.api import PythonAlgorithm, AlgorithmFactory, MatrixWorkspaceProperty, FileProperty, FileAction, PropertyMode
from mantid.kernel import StringListValidator, StringMandatoryValidator, Direction, logger
from mantid import config
import os.path

class IndirectAnnulusAbsorption(PythonAlgorithm):
 
    def category(self):
        return "Workflow\\MIDAS;PythonAlgorithms"

    def PyInit(self):
        self.declareProperty(name='Sample Input', defaultValue='Workspace', validator=StringListValidator(['Workspace','File']),
            doc='Sample input type')
        self.declareProperty(MatrixWorkspaceProperty('Sample Workspace', '', optional=PropertyMode.Optional, 
            direction=Direction.Input), doc="Name for the input Sample workspace.")
        self.declareProperty(FileProperty('Sample File', '', action=FileAction.OptionalLoad, extensions=["_red.nxs"]),
                             doc='File path for Sample file')

        self.declareProperty(name='Use Can', defaultValue=False, doc = 'Use Can')
        self.declareProperty(name='Can Input', defaultValue='Workspace', validator=StringListValidator(['Workspace','File']),
            doc='Can input type')
        self.declareProperty(MatrixWorkspaceProperty('Can Workspace', '', optional=PropertyMode.Optional, 
            direction=Direction.Input), doc="Name for the input Can workspace.")
        self.declareProperty(FileProperty('Can File', '', action=FileAction.OptionalLoad, extensions=["_red.nxs"]),
                             doc='File path for Can file')
        self.declareProperty(name='Can scale factor', defaultValue='1.0', doc = 'Scale factor to multiply can data')

        self.declareProperty(name='Chemical formula', defaultValue='', doc = 'Chemical formula')
        self.declareProperty(name='Can inner radius', defaultValue='', doc = 'Sample radius')
        self.declareProperty(name='Sample inner radius', defaultValue='', doc = 'Sample radius')
        self.declareProperty(name='Sample outer radius', defaultValue='', doc = 'Sample radius')
        self.declareProperty(name='Can outer radius', defaultValue='', doc = 'Sample radius')
        self.declareProperty(name='Sample number density', defaultValue='', doc = 'Sample number density')
        self.declareProperty(name='Events', defaultValue=5000, doc = 'Number of neutron events')
        self.declareProperty(name='Verbose', defaultValue=False, doc = 'Switch Verbose Off/On')
        self.declareProperty(name='Plot', defaultValue=False, doc = 'Plot options')
        self.declareProperty(name='Save', defaultValue=False, doc = 'Switch Save result to nxs file Off/On')
 
    def PyExec(self):

        from IndirectCommon import StartTime, EndTime, getEfixed, addSampleLogs
        from IndirectImport import import_mantidplot
        mp = import_mantidplot()

        StartTime('Cylinder Absorption')
        workdir = config['defaultsave.directory']
        self._setup()
        efixed = getEfixed(self._sam)                # Get efixed
        swaveWS = '__sam_wave'
        ConvertUnits(InputWorkspace=self._sam, OutputWorkspace=swaveWS, Target='Wavelength',
            EMode='Indirect', EFixed=efixed)

        name = self._sam[:-4]
        assWS = name + '_ann_ass'
        corrWS = name + '_corrected'
        AnnularRingAbsorption(InputWorkspace=swaveWS, OutputWorkspace=assWS,
            SampleHeight=3.0, SampleThickness=self._radius3-self._radius2, 
            CanInnerRadius=self._radius1,CanOuterRadius=self._radius4,
            SampleChemicalFormula=self._chem,SampleNumberDensity=self._density,
            NumberOfWavelengthPoints=10,EventsPerPoint=self._events)
        plot_list = [corrWS, self._sam]

        if self._usecan:
            cwaveWS = '__can_wave'
            ConvertUnits(InputWorkspace=self._can, OutputWorkspace=cwaveWS, Target='Wavelength',
                EMode='Indirect', EFixed=efixed)
            if self._can_scale != 1.0:
                if self._verbose:
                    logger.notice('Scaling can by : '+str(self._can_scale))
                Scale(InputWorkspace=cwaveWS, OutputWorkspace=cwaveWS, Factor=self._can_scale, Operation='Multiply')
            Minus(LHSWorkspace=swaveWS, RHSWorkspace=cwaveWS, OutputWorkspace=swaveWS)
            plot_list.append(self._can)

        Divide(LHSWorkspace=swaveWS, RHSWorkspace=assWS, OutputWorkspace=swaveWS) 
        ConvertUnits(InputWorkspace=swaveWS, OutputWorkspace=corrWS, Target='DeltaE',
            EMode='Indirect', EFixed=efixed)
        sample_logs = {'sample_shape': 'annulus', 'sample_filename': self._sam,
                        'sample_inner': self._radius2, 'sample_outer': self._radius3,
                        'can_inner': self._radius1, 'can_outer': self._radius4}
        addSampleLogs(assWS, sample_logs)
        addSampleLogs(corrWS, sample_logs)
        if self._usecan:
		    AddSampleLog(Workspace=assWS, LogName='can_filename', LogType='String', LogText=str(self._can))
		    AddSampleLog(Workspace=corrWS, LogName='can_filename', LogType='String', LogText=str(self._can))
		    AddSampleLog(Workspace=assWS, LogName='can_scale', LogType='String', LogText=str(self._can_scale))
		    AddSampleLog(Workspace=corrWS, LogName='can_scale', LogType='String', LogText=str(self._can_scale))

        if self._plot:
            mp.plotSpectrum(plot_list, 0)

        if self._save:
            path = os.path.join(workdir,corrWS + '.nxs')
            SaveNexusProcessed(InputWorkspace=corrWS, Filename=path)
            if self._verbose:
                logger.notice('Output file created : '+path)

        EndTime('Cylinder Absorption')

    def _setup(self):
        self._verbose = self.getProperty('Verbose').value
        sInput = self.getPropertyValue('Sample Input')
        if sInput == 'Workspace':
            s_ws = self.getPropertyValue('Sample Workspace')
        else:
            s_ws = ''
        if sInput == 'File':
            s_file = self.getPropertyValue('Sample File')
        else:
            s_file = ''
        self._input = sInput
        self._path = s_file
        self._ws = s_ws
        self._getData()
        self._sam = self._name

        self._usecan = self.getProperty('Use can').value
        if self._usecan:
            cInput = self.getPropertyValue('Can Input')
            if cInput == 'Workspace':
                c_ws = self.getPropertyValue('Can Workspace')
            else:
                c_ws = ''
            if cInput == 'File':
                c_file = self.getPropertyValue('Can File')
            else:
                c_file = ''
            self._input = cInput
            self._path = c_file
            self._ws = c_ws
            self._getData()
            self._can = self._name
            self._can_scale = self.getPropertyValue('Can scale factor')
 
        self._chem = self.getPropertyValue('Chemical formula')
        self._density = self.getPropertyValue('Sample number density')
        self._radius1 = float(self.getPropertyValue('Can inner radius'))
        self._radius2 = float(self.getPropertyValue('Sample inner radius'))
        self._radius3 = float(self.getPropertyValue('Sample outer radius'))
        self._radius4 = float(self.getPropertyValue('Can outer radius'))
        self._events = self.getPropertyValue('Events')
        self._plot = self.getProperty('Plot').value
        self._save = self.getProperty('Save').value
		
    def _getData(self):   #get data
        if self._input == 'Workspace':
            inWS = self._ws
            self._name = inWS
            if self._verbose:
                logger.notice('Input from Workspace : '+inWS)
        elif self._input == 'File':
            self._getFileName()
            inWS = self._name
            LoadNexus(Filename=self._path, OutputWorkspace=inWS)
        else:
            raise ValueError('Input type not defined')

    def _getFileName(self):
        import os.path
        path = self._path
        if(os.path.isfile(path)): 
            base = os.path.basename(path)
            self._name = os.path.splitext(base)[0]
            ext = os.path.splitext(base)[1]
            if self._verbose:
                logger.notice('Input file : '+path)
        else:
            raise ValueError('Could not find file: ' + path)


# Register algorithm with Mantid
AlgorithmFactory.subscribe(IndirectAnnulusAbsorption)
#
