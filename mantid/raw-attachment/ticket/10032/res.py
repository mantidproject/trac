def calculate_resolution(input_data, mass, index=0):
    """
        Run the VesuvioResolution function to produce a workspace
        with the value of the Vesuvio resolution. 

        @param input_data The original TOF data
        @param mass The mass defining the recoil peak in AMU
    """
    from mantid.simpleapi import AlgorithmManager, mtd
    
    name_stem = str(input_data)
    output_name = name_stem + "_resolution"
    function = "name=VesuvioResolution, Mass=%f" % mass
    
    # execute the resolution function using fit.
    # functions can't currently be executed as stand alone objects,
    # so for now we will run fit with zero iterations to achieve the same result.
    fit = mantid.api.AlgorithmManager.createUnmanaged('Fit')        
    fit.initialize()
    fit.setChild(True)
    fit.setAlwaysStoreInADS(True)
    fit.setLogging(False)
    mantid.simpleapi._set_properties(fit, function, input_data, MaxIterations=0, 
                                     CreateOutput=True, Output=name_stem)
    fit.execute()

    ExtractSingleSpectrum(name_stem + "_Workspace", WorkspaceIndex=1, OutputWorkspace=output_name)

    DeleteWorkspace(name_stem + "_Workspace")
    DeleteWorkspace(name_stem + "_Parameters")
    DeleteWorkspace(name_stem + "_NormalisedCovarianceMatrix")

    return mtd[output_name]

	
runs = "14189-14195"
spectra = "135"
diff_type="SingleDifference" # Allowed values=Single,Double,Thick
ip_file = "IP0004_10.par"

raw_ws = LoadVesuvio(Filename=runs, SpectrumList=spectra,
				   Mode=diff_type,InstrumentParFile=ip_file)
raw_ws = CropWorkspace(raw_ws,XMin=50.0,XMax=562.0)
y_workspace = ConvertToYSpace(raw_ws, Mass=1.0076)
calculate_resolution(y_workspace, 1.0067, 0)
