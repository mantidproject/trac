import time

# Run SXD_NaCl (in the scripts dir) in order to generate intput  for the following.
svw = plotSlice('QLab')
sv = svw.getSlicer()
sv.setPeaksWorkspaces(['peaks_qLab', 'peaks_qLab_Integrated'])
time.sleep(2)
sv.clearPeaksWorkspaces()
time.sleep(2)
sv.setPeaksWorkspaces(['peaks_qLab_Integrated'])