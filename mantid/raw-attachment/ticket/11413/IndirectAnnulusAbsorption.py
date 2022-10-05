from mantid.simpleapi import *
from mantid.api import DataProcessorAlgorithm, AlgorithmFactory, MatrixWorkspaceProperty, PropertyMode
from mantid.kernel import StringMandatoryValidator, Direction, logger


class IndirectAnnulusAbsorption(DataProcessorAlgorithm):

    def category(self):
        return "Workflow\\Inelastic;PythonAlgorithms;CorrectionFunctions\\AbsorptionCorrections;Workflow\\MIDAS"


    def summary(self):
        return "Calculates indirect absorption corrections for an annulus sample shape."


    def PyInit(self):
        self.declareProperty(MatrixWorkspaceProperty('SampleWorkspace', '', direction=Direction.Input),
                             doc='Sample workspace.')

        self.declareProperty(name='SampleChemicalFormula', defaultValue='', validator=StringMandatoryValidator(),
                             doc='Chemical formula for the sample')
        self.declareProperty(name='SampleNumberDensity', defaultValue=0.1, doc='Sample number density')
        self.declareProperty(name='SampleInnerRadius', defaultValue=0.0, doc='Sample radius')
        self.declareProperty(name='SampleOuterRadius', defaultValue=0.0, doc='Sample radius')

        self.declareProperty(MatrixWorkspaceProperty('CanWorkspace', '', optional=PropertyMode.Optional,
                                                     direction=Direction.Input),
                             doc='Container workspace.')
        self.declareProperty(name='UseCanCorrections', defaultValue=False, doc='Use can corrections in subtraction')
        self.declareProperty(name='CanChemicalFormula', defaultValue='', validator=StringMandatoryValidator(),
                             doc='Chemical formula for the can')
        self.declareProperty(name='CanNumberDensity', defaultValue=0.1, doc='Can number density')
        self.declareProperty(name='CanInnerRadius', defaultValue=0.0, doc='Sample radius')
        self.declareProperty(name='CanOuterRadius', defaultValue=0.0, doc='Sample radius')
        self.declareProperty(name='CanScaleFactor', defaultValue=1.0, doc='Scale factor to multiply can data')

        self.declareProperty(name='Events', defaultValue=5000, doc='Number of neutron events')
        self.declareProperty(name='Plot', defaultValue=False, doc='Plot options')

        self.declareProperty(MatrixWorkspaceProperty('OutputWorkspace', '', direction=Direction.Output),
                             doc='The output corrected workspace.')

        self.declareProperty(MatrixWorkspaceProperty('CorrectionsWorkspace', '', direction=Direction.Output,
                                                     optional=PropertyMode.Optional),
                             doc='The corrections workspace for scattering and absorptions in sample.')


    def PyExec(self):
        from IndirectCommon import getEfixed, addSampleLogs

        self._setup()

        efixed = getEfixed(self._sample_ws_name)

        sample_wave_ws = '__sam_wave'
        ConvertUnits(InputWorkspace=self._sample_ws_name, OutputWorkspace=sample_wave_ws,
                     Target='Wavelength', EMode='Indirect', EFixed=efixed)

        sample_thickness = self._sample_outer_radius - self._sample_inner_radius
        logger.information('Sample thickness: ' + str(sample_thickness))

        AnnularRingAbsorption(InputWorkspace=sample_wave_ws,
                              OutputWorkspace=self._ass_ws,
                              SampleHeight=3.0,
                              SampleThickness=sample_thickness,
                              CanInnerRadius=self._can_inner_radius,
                              CanOuterRadius=self._can_outer_radius,
                              SampleChemicalFormula=self._sample_chemical_formula,
                              SampleNumberDensity=self._sample_number_density,
                              NumberOfWavelengthPoints=10,
                              EventsPerPoint=self._events)

        plot_data = [self._output_ws, self._sample_ws_name]
        plot_corr = [self._ass_ws]
        group = self._ass_ws

        if self._can_ws_name is not None:
            can1_wave_ws = '__can1_wave'
            can2_wave_ws = '__can2_wave'
            ConvertUnits(InputWorkspace=self._can_ws_name, OutputWorkspace=can1_wave_ws,
                         Target='Wavelength', EMode='Indirect', EFixed=efixed)
            if self._can_scale != 1.0:
                logger.information('Scaling can by: ' + str(self._can_scale))
                Scale(InputWorkspace=can1_wave_ws, OutputWorkspace=can1_wave_ws, Factor=self._can_scale, Operation='Multiply')
            CloneWorkspace(InputWorkspace=can1_wave_ws, OutputWorkspace=can2_wave_ws)

            can_thickness1 = self._sample_inner_radius - self._can_inner_radius
            can_thickness2 = self._can_outer_radius - self._sample_outer_radius
            logger.information('Can thickness: ' + str(can_thickness1) + ' & ' + str(can_thickness2))

            if self._use_can_corrections:
                Divide(LHSWorkspace=sample_wave_ws, RHSWorkspace=self._ass_ws, OutputWorkspace=sample_wave_ws)

                SetSampleMaterial(can1_wave_ws, ChemicalFormula=self._can_chemical_formula, SampleNumberDensity=self._can_number_density)
                AnnularRingAbsorption(InputWorkspace=can1_wave_ws,
                              OutputWorkspace='__Acc1',
                              SampleHeight=3.0,
                              SampleThickness=can_thickness1,
                              CanInnerRadius=self._can_inner_radius,
                              CanOuterRadius=self._sample_outer_radius,
                              SampleChemicalFormula=self._can_chemical_formula,
                              SampleNumberDensity=self._can_number_density,
                              NumberOfWavelengthPoints=10,
                              EventsPerPoint=self._events)
                SetSampleMaterial(can2_wave_ws, ChemicalFormula=self._can_chemical_formula, SampleNumberDensity=self._can_number_density)
                AnnularRingAbsorption(InputWorkspace=can2_wave_ws,
                              OutputWorkspace='__Acc2',
                              SampleHeight=3.0,
                              SampleThickness=can_thickness2,
                              CanInnerRadius=self._sample_inner_radius,
                              CanOuterRadius=self._can_outer_radius,
                              SampleChemicalFormula=self._can_chemical_formula,
                              SampleNumberDensity=self._can_number_density,
                              NumberOfWavelengthPoints=10,
                              EventsPerPoint=self._events)
                Multiply(LHSWorkspace='__Acc1', RHSWorkspace='__Acc2', OutputWorkspace=self._acc_ws)
                Divide(LHSWorkspace=can1_wave_ws, RHSWorkspace=self._acc_ws, OutputWorkspace=can1_wave_ws)
                Minus(LHSWorkspace=sample_wave_ws, RHSWorkspace=can1_wave_ws, OutputWorkspace=sample_wave_ws)
                plot_corr.append(self._acc_ws)
                group += ',' + self._acc_ws

            else:
                Minus(LHSWorkspace=sample_wave_ws, RHSWorkspace=can1_wave_ws, OutputWorkspace=sample_wave_ws)
                Divide(LHSWorkspace=sample_wave_ws, RHSWorkspace=self._ass_ws, OutputWorkspace=sample_wave_ws)

                DeleteWorkspace(can1_wave_ws)
                DeleteWorkspace(can2_wave_ws)
                plot_data.append(self._can_ws_name)

        else:
            Divide(LHSWorkspace=sample_wave_ws, RHSWorkspace=self._ass_ws, OutputWorkspace=sample_wave_ws)

        ConvertUnits(InputWorkspace=sample_wave_ws, OutputWorkspace=self._output_ws, Target='DeltaE',
                     EMode='Indirect', EFixed=efixed)
        DeleteWorkspace(sample_wave_ws)

        sample_logs = {'sample_shape': 'annulus',
                       'sample_filename': self._sample_ws_name,
                       'sample_inner': self._sample_inner_radius,
                       'sample_outer': self._sample_outer_radius,
                       'can_inner': self._can_inner_radius,
                       'can_outer': self._can_outer_radius}
        addSampleLogs(self._ass_ws, sample_logs)
        addSampleLogs(self._output_ws, sample_logs)

        if self._can_ws_name is not None:
            AddSampleLog(Workspace=self._output_ws, LogName='can_filename', LogType='String', LogText=str(self._can_ws_name))
            AddSampleLog(Workspace=self._output_ws, LogName='can_scale', LogType='String', LogText=str(self._can_scale))
            if self._use_can_corrections:
                addSampleLogs(self._acc_ws, sample_logs)
                AddSampleLog(Workspace=self._acc_ws, LogName='can_filename', LogType='String', LogText=str(self._can_ws_name))
                AddSampleLog(Workspace=self._acc_ws, LogName='can_scale', LogType='String', LogText=str(self._can_scale))
                AddSampleLog(Workspace=self._output_ws, LogName='can_thickness1', LogType='String', LogText=str(can_thickness1))
                AddSampleLog(Workspace=self._output_ws, LogName='can_thickness2', LogType='String', LogText=str(can_thickness2))

        self.setProperty('OutputWorkspace', self._output_ws)

        # Output the Ass workspace if it is wanted, delete if not
        if self._abs_ws == '':
            DeleteWorkspace(self._ass_ws)
            if self._can_ws_name is not None:
                if self._use_can_corrections:
                    DeleteWorkspace(self._acc_ws)
        else:
            group_name = self._abs_ws + '_abs'
            GroupWorkspaces(InputWorkspaces=group, OutputWorkspace=group_name)
            self.setProperty('CorrectionsWorkspace', group_name)

        if self._plot:
            from IndirectImport import import_mantidplot
            mantid_plot = import_mantidplot()
            mantid_plot.plotSpectrum(plot_data, 0)
            mantid_plot.plotSpectrum(plot_corr, 0)


    def _setup(self):
        """
        Get algorithm properties.
        """

        self._sample_ws_name = self.getPropertyValue('SampleWorkspace')
        self._sample_chemical_formula = self.getPropertyValue('SampleChemicalFormula')
        self._sample_number_density = self.getProperty('SampleNumberDensity').value
        self._sample_inner_radius = self.getProperty('SampleInnerRadius').value
        self._sample_outer_radius = self.getProperty('SampleOuterRadius').value

        self._can_ws_name = self.getPropertyValue('CanWorkspace')
        if self._can_ws_name == '':
            self._can_ws_name = None
        self._use_can_corrections = self.getProperty('UseCanCorrections').value
        self._can_chemical_formula = self.getPropertyValue('CanChemicalFormula')
        self._can_number_density = self.getProperty('CanNumberDensity').value
        self._can_inner_radius = self.getProperty('CanInnerRadius').value
        self._can_outer_radius = self.getProperty('CanOuterRadius').value
        self._can_scale = self.getProperty('CanScaleFactor').value

        self._events = self.getProperty('Events').value
        self._plot = self.getProperty('Plot').value
        self._output_ws = self.getPropertyValue('OutputWorkspace')

        self._abs_ws = self.getPropertyValue('CorrectionsWorkspace')
        if self._abs_ws == '':
            self._ass_ws = '__ass'
            self._acc_ws = '__acc'
        else:
            self._ass_ws = self._abs_ws + '_ass'
            self._acc_ws = self._abs_ws + '_acc'

# Register algorithm with Mantid
AlgorithmFactory.subscribe(IndirectAnnulusAbsorption)
