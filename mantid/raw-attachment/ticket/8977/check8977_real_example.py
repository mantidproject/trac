# add ndxsans2d/user/Masks  and cycle 13_3 to directory manager.
import ISISCommandInterface as ici
import math
MASKFILE = FileFinder.getFullPath('MASKSANS2D_133F_12m_8mm_Hellsing_changer.txt')
assert(MASKFILE)
ici.SANS2D()
ici.MaskFile(MASKFILE)
ici.TransFit('Polynomial3')
ici.AssignSample('21012')
ici.TransmissionSample('21005','21002')
reduced = ici.WavRangeReduction()

name = '21005_trans_sample_1.5_12.5'
b = plotSpectrum(name + '_unfitted',0,True)
plotSpectrum(name, 0, True, window=b)