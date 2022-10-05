

#
# Exclude the monitors when loading the raw SXD file.  This avoids 
#
SXD23767=Load(Filename='SXD23767.raw',LoadMonitors='Exclude')

#
# A lower SplitThreshold, with a reasonable bound on the recursion depth, helps find weaker peaks at higher Q.
#
#QLab = ConvertToMD(InputWorkspace=SXD23767,OutputWorkspace='QLab',QDimensions='Q3D',dEAnalysisMode='Elastic',MinValues='-15,-15,-15',MaxValues='15,15,15',SplitThreshold='50',MaxRecursionDepth='13')
QLab = ConvertToDiffractionMDWorkspace(InputWorkspace=SXD23767, OutputDimensions='Q (lab frame)', SplitThreshold=50, LorentzCorrection='1',MaxRecursionDepth='13',Extents='-15,15,-15,15,-15,15')
#
#  NaCl has a relatively small unit cell, so the distance between peaks is relatively large.  Setting the PeakDistanceThreshold
#  higher avoids finding high count regions on the sides of strong peaks as separate peaks.
#
peaks_qLab = FindPeaksMD(InputWorkspace='QLab', MaxPeaks=300, DensityThresholdFactor=10,PeakDistanceThreshold=1.0)

binned = BinMD(InputWorkspace=QLab,AlignedDim0='Q_lab_x,-10,10,300',AlignedDim1='Q_lab_y,-10,10,300',AlignedDim2='Q_lab_z,-10,10,300')

clusters = IntegratePeaksUsingClusters(InputWorkspace=binned, PeaksWorkspace=peaks_qLab, Threshold=10000)
