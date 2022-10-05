from isis_reflectometry import quick
reload(quick)
run_1 = Load('POLREF00008481.nxs')
run_2 = Load('POLREF00008481.nxs')
run_3 = Load('POLREF00008481.nxs')
run_4 = Load('POLREF00008481.nxs')

runs = GroupWorkspaces(InputWorkspaces='run_1, run_2, run_3, run_4')

mytemp = SumSpectra(InputWorkspace=runs, StartWorkspaceIndex=3, EndWorkspaceIndex=644)

#out = quick.quick(run=runs, theta=0.4, detector_component_name='lineardetector', polcorr=2, correct_positions=False  )

a, b, c = ReflectometryReductionOneAuto(InputWorkspace=runs, ThetaIn=0.4, CorrectDetectorPositions=False, PolarizationAnalysis='PA')