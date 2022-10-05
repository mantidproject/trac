Load(Filename=r'INTER00020681.nxs',OutputWorkspace='_sum')
RenameWorkspace(InputWorkspace='_sum',OutputWorkspace='_W')
ConvertUnits(InputWorkspace='_W',OutputWorkspace='_W_lam',Target='Wavelength',AlignBins='1')
CropWorkspace(InputWorkspace='_W_lam',OutputWorkspace='_M',EndWorkspaceIndex='2')
CalculateFlatBackground(InputWorkspace='_M',OutputWorkspace='_M',StartX='15',EndX='17',WorkspaceIndexList='1')
CropWorkspace(InputWorkspace='_W_lam',OutputWorkspace='_DP',XMin='1',XMax='17',StartWorkspaceIndex='3',EndWorkspaceIndex='4')
RebinToWorkspace(WorkspaceToRebin='_M',WorkspaceToMatch='_DP',OutputWorkspace='_M_P')
CropWorkspace(InputWorkspace='_M_P',OutputWorkspace='_I0P',StartWorkspaceIndex='2',EndWorkspaceIndex='2')
PolynomialCorrection(InputWorkspace='_DP',OutputWorkspace='IvsLam',Coefficients='35.5893,-24.5591,9.20375,-1.89265,0.222291,-0.0148746,0.00052709,-7.66807e-06',Operation='Divide')
Divide(LHSWorkspace='IvsLam',RHSWorkspace='_I0P',OutputWorkspace='IvsLam')
ConvertUnits(InputWorkspace='IvsLam',OutputWorkspace='IvsQ',Target='MomentumTransfer')
RenameWorkspace(InputWorkspace='IvsQ',OutputWorkspace='20681_IvsQ')
Rebin(InputWorkspace='20681_IvsQ',OutputWorkspace='20681_IvsQ_binned',Params='0.034,-0.05,0.341484')
