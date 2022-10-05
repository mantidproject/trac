LoadMD(Filename='SEQ_MDEW.nxs', OutputWorkspace='SEQ')
# Rebinned 4D MDHistoWorkspace
SliceMD(InputWorkspace='SEQ', AlignedDimX='[Qh,0,0],0,0.5,20', AlignedDimY='[0.5Qh,0.866Qk,0],-0.75,-0.25,20', AlignedDimZ='[0,0,Ql],-0.9,-0.55,20', AlignedDimT='DeltaE,17,22,20', OutputWorkspace='SEQ_4D_rebin')
# Rebinned 4D->3D MDHistoWorkspace
SliceMD(InputWorkspace='SEQ', AlignedDimX='[Qh,0,0],0,0.5,20', AlignedDimY='DeltaE,17,22,20', AlignedDimZ='[0.5Qh,0.866Qk,0],-0.75,-0.25,20', OutputWorkspace='SEQ_3D_rebin')
# Rebinned 4D->2D MDHistoWorkspace
SliceMD(InputWorkspace='SEQ', AlignedDimX='[Qh,0,0],0,0.5,20', AlignedDimY='DeltaE,17,22,20', OutputWorkspace='SEQ_2D_rebin')
# Rebinned 4D->1D MDHistoWorkspace
SliceMD(InputWorkspace='SEQ', AlignedDimX='DeltaE,17,22,20', OutputWorkspace='SEQ_1D_rebin')
# Integrated 4D->3D MDHistoWorkspace
SliceMD(InputWorkspace='SEQ', AlignedDimX='[Qh,0,0],0,0.5,20', AlignedDimY='DeltaE,17,22,20', AlignedDimZ='[0.5Qh,0.866Qk,0],-0.75,-0.25,20', AlignedDimT='[0,0,Ql],-0.9,-0.55,1', OutputWorkspace='SEQ_3D_int')
# Integrated 4D->2D MDHistoWorkspace
SliceMD(InputWorkspace='SEQ', AlignedDimX='[Qh,0,0],0,0.5,20', AlignedDimY='DeltaE,17,22,20', AlignedDimZ='[0.5Qh,0.866Qk,0],-0.75,-0.25,1', AlignedDimT='[0,0,Ql],-0.9,-0.55,1', OutputWorkspace='SEQ_2D_int')
# Integrated 4D->1D MDHistoWorkspace
SliceMD(InputWorkspace='SEQ', AlignedDimX='DeltaE,17,22,20', AlignedDimY='[Qh,0,0],0,0.5,1', AlignedDimZ='[0.5Qh,0.866Qk,0],-0.75,-0.25,1', AlignedDimT='[0,0,Ql],-0.9,-0.55,1', OutputWorkspace='SEQ_1D_int')
