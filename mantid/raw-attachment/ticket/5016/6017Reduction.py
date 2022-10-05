from mantidsimple import *

######################################################################
Load(Filename=r'POLREF00006017.nxs',OutputWorkspace='POLREF00006017')

PIX=1.1E-3 #
SC=96 #Reflected line
avgDB=27 #Transmission

X=mtd['POLREF00006017']
ConvertUnits(InputWorkspace=X,OutputWorkspace=X,Target="Wavelength",AlignBins="1")
CropWorkspace(InputWorkspace=X,OutputWorkspace='Io',XMin=1,XMax=14.5,StartWorkspaceIndex=2,EndWorkspaceIndex=2) #Monitor
CropWorkspace(InputWorkspace=X,OutputWorkspace='D',XMin=1,XMax=14.5,StartWorkspaceIndex=3) #Start detectors
Io=mtd['Io']
D=mtd['D']

Divide(D,Io,'I','1','1')
I=mtd['I']

# Move the detector so that the detector channel matching the reflected beam is at 0,0
MoveInstrumentComponent(Workspace=I,ComponentName="lineardetector",X=0,Y=0,Z=-PIX*( (SC-avgDB)/2.0 +avgDB) )

#CloneWorkspace(I,'I2')
ConvertSpectrumAxis(InputWorkspace=I,OutputWorkspace='SignedTheta_vs_Wavelength',Target='signed_theta')

#  Run MD Conversions
ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='QxQy',OutputDimensions='Q (lab frame)', Extents='-0.0005,0.0005,0,0.12')
ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='KiKf',OutputDimensions='K (incident, final)', Extents='0,0.05,0,0.05')
ConvertToReflectometryQ(InputWorkspace='SignedTheta_vs_Wavelength',OutputWorkspace='PiPf',OutputDimensions='P (lab frame)', Extents='0,0.1,-0.02,0.15')

# Bin Outputs to MD Histogam Workspaces
BinMD(InputWorkspace='QxQy',AxisAligned='0',BasisVector0='Qx,(Ang^-1),1,0',BasisVector1='Qz,(Ang^-1),0,1',OutputExtents='-0.0005,0.0005,0,0.12',OutputBins='100,100',Parallel='1',OutputWorkspace='QxQy_rebinned')
BinMD(InputWorkspace='KiKf',AxisAligned='0',BasisVector0='Ki,(Ang^-1),1,0',BasisVector1='Kf,(Ang^-1),0,1',OutputExtents='0,0.05,0,0.05',OutputBins='200,200',Parallel='1',OutputWorkspace='KiKf__rebinned')
BinMD(InputWorkspace='PiPf',AxisAligned='0',BasisVector0='Pz_i + Pz_f,(Ang^-1),1,0',BasisVector1='Pz_i - Pz_f,(Ang^-1),0,1',OutputExtents='0,0.1,-0.02,0.15',OutputBins='50,50',Parallel='1',OutputWorkspace='PiPf_rebinned')
