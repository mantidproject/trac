def align(wksp, preserveEvents):
    AlignAndFocusPowder(InputWorkspace=wksp,OutputWorkspace=wksp,
                        CalFileName='/SNS/PG3/2013_2_11A_CAL/PG3_PAC_d15024_2013_08_22.cal',
                        Params=-0.0004,#DMin=2.,DMax=15.35,
                        TMin=66666.67,TMax=83333.67,
                        PreserveEvents=preserveEvents,RemovePromptPulseWidth=50.)


for state in (True, False):
    Load(Filename='/SNS/PG3/IPTS-2767/0/15138/NeXus/PG3_15138_event.nxs',OutputWorkspace='PG3_15138')
    FilterBadPulses(InputWorkspace='PG3_15138',OutputWorkspace='PG3_15138')
    CompressEvents(InputWorkspace='PG3_15138', OutputWorkspace='PG3_15138', Tolerance=.01)
    NormaliseByCurrent(InputWorkspace='PG3_15138',OutputWorkspace='PG3_15138')
    if state:
        # test the difference between using SetSampleMaterial and not
        align('PG3_15138',False)
        
        MultipleScatteringCylinderAbsorption(InputWorkspace='PG3_15138',OutputWorkspace='hand_set')
        SetSampleMaterial(InputWorkspace='PG3_15138',ChemicalFormula='V',SampleNumberDensity=0.0721)
        MultipleScatteringCylinderAbsorption(InputWorkspace='PG3_15138',OutputWorkspace='set_sample')

        ConvertUnits(InputWorkspace='PG3_15138',OutputWorkspace='PG3_15138',Target='dSpacing')
        ConvertUnits(InputWorkspace='hand_set',OutputWorkspace='hand_set',Target='dSpacing')
        ConvertUnits(InputWorkspace='set_sample',OutputWorkspace='set_sample',Target='dSpacing')

    else:
        # test the difference between correcting before and after grouping
        SetSampleMaterial(InputWorkspace='PG3_15138',ChemicalFormula='V',SampleNumberDensity=0.0721)
        MultipleScatteringCylinderAbsorption(InputWorkspace='PG3_15138',OutputWorkspace='separate')
        align('separate',True)

        align('PG3_15138',True)
        MultipleScatteringCylinderAbsorption(InputWorkspace='PG3_15138',OutputWorkspace='together')

        ConvertUnits(InputWorkspace='PG3_15138',OutputWorkspace='PG3_15138',Target='dSpacing')
        ConvertUnits(InputWorkspace='separate',OutputWorkspace='separate',Target='dSpacing')
        ConvertUnits(InputWorkspace='together',OutputWorkspace='together',Target='dSpacing')
