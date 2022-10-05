def  runAlgorithm():
        workspace_name = "POLREF00004699"
        workspace_nexus_file = workspace_name + ".nxs"
        
        PIX=1.1E-3 #m
        SC=75
        avgDB=29
        Load(Filename=workspace_nexus_file,OutputWorkspace=workspace_name)
        X=mtd[workspace_name]
        X = ConvertUnits(InputWorkspace=X,Target="Wavelength",AlignBins="1")
        # Reference intensity to normalise by
        CropWorkspace(InputWorkspace=X,OutputWorkspace='Io',XMin=0.8,XMax=14.5,StartWorkspaceIndex=2,EndWorkspaceIndex=2)
        # Crop out transmission and noisy data 
        CropWorkspace(InputWorkspace=X,OutputWorkspace='D',XMin=0.8,XMax=14.5,StartWorkspaceIndex=3)
        Io=mtd['Io']
        D=mtd['D']
    
        # Peform the normaisation step
        Divide(LHSWorkspace=D,RHSWorkspace=Io,OutputWorkspace='I',
               AllowDifferentNumberSpectra='1',ClearRHSWorkspace='1')
        I=mtd['I'][0]
        
        # Automatically determine the SC and averageDB 
        FindReflectometryLines(InputWorkspace=I, StartWavelength=10, OutputWorkspace='spectrum_numbers')
        spectrum_table = mtd['spectrum_numbers']
        
        # Move the detector so that the detector channel matching the reflected beam is at 0,0
        MoveInstrumentComponent(Workspace=I,ComponentName="lineardetector",X=0,Y=0,Z=-PIX*( (SC-avgDB)/2.0 +avgDB) )
        
        # Should now have signed theta vs Lambda
        ConvertSpectrumAxis(InputWorkspace=I,OutputWorkspace='SignedTheta_vs_Wavelength',Target='signed_theta')
        
        # Check that signed two theta is being caluclated correctly (not normalised)
        ws1 = mtd['SignedTheta_vs_Wavelength']
        upperHistogram = ws1.getNumberHistograms()-1
        # MD transformations
        ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='QxQyMD',OutputDimensions='Q (lab frame)', Extents='-0.0005,0.0005,0,0.12')
        ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='QxQy2D',OutputDimensions='Q (lab frame)', NumberBinsQx=100, NumberBinsQz=100, OutputAsMDWorkspace=False, Extents='-0.0005,0.0005,0,0.12')
        
	ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='KiKfMD',OutputDimensions='K (incident, final)', Extents='0,0.05,0,0.05')
	ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='KiKf2D',OutputDimensions='K (incident, final)', Extents='0,0.05,0,0.05', NumberBinsQx=100, NumberBinsQz=100, OutputAsMDWorkspace=False)
        
	ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='PiPfMD',OutputDimensions='P (lab frame)', Extents='0,0.1,-0.02,0.15')
	ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='PiPf2D',OutputDimensions='P (lab frame)', Extents='0,0.1,-0.02,0.15', NumberBinsQx=100, NumberBinsQz=100, OutputAsMDWorkspace=False)
	
	BinMD(InputWorkspace='QxQyMD',AxisAligned='0',BasisVector0='Qx,(Ang^-1),1,0',BasisVector1='Qz,(Ang^-1),0,1',OutputExtents='-0.0005,0.0005,0,0.12',OutputBins='100,100',Parallel='1',OutputWorkspace='QxQy_rebinned')
        BinMD(InputWorkspace='KiKfMD',AxisAligned='0',BasisVector0='Ki,(Ang^-1),1,0',BasisVector1='Kf,(Ang^-1),0,1',OutputExtents='0,0.05,0,0.05',OutputBins='100,100',Parallel='1',OutputWorkspace='KiKf_rebinned')
        BinMD(InputWorkspace='PiPfMD',AxisAligned='0',BasisVector0='Pz_i + Pz_f,(Ang^-1),1,0',BasisVector1='Pz_i - Pz_f,(Ang^-1),0,1',OutputExtents='0,0.1,-0.02,0.15',OutputBins='100,100',Parallel='1',OutputWorkspace='PiPf_rebinned')
       
runAlgorithm()

#Comparision 1
plotSlice(source='QxQy_rebinned', colormin=2e2, colormax=3e9, colorscalelog=True)
plotSlice(source='QxQy2D', colormin=2e2, colormax=3e9, colorscalelog=True)

#Comparision 2
plotSlice(source='KiKf_rebinned', colormin=2e2, colormax=3e9, colorscalelog=True)
plotSlice(source='KiKf2D', colormin=2e2, colormax=3e9, colorscalelog=True)

#Comparision 3
plotSlice(source='PiPf_rebinned', colormin=2e2, colormax=3e9, colorscalelog=True)
plotSlice(source='PiPf2D', colormin=2e2, colormax=3e9, colorscalelog=True)
