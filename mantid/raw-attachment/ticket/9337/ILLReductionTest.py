run_name = 'ILLIN16B_034745'
kwargs = {}
kwargs['Run'] = run_name + '.nxs'
kwargs['Analyser'] = 'silicon'
kwargs['Reflection'] = '111'
kwargs['RawWorkspace'] = run_name + '_' + kwargs['Analyser'] + kwargs['Reflection'] + '_raw'
kwargs['ReducedWorkspace'] = run_name + '_' + kwargs['Analyser'] + kwargs['Reflection'] + '_red'
kwargs['Verbose'] = True

IndirectILLReduction(**kwargs)