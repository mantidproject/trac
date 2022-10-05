Load(Filename=r'C:\mantidbuild\ExternalData\Testing\Data\DocTest\INTER00013463.nxs', OutputWorkspace='INTER00013463')
ConvertSpectrumAxis(InputWorkspace='INTER00013463', OutputWorkspace='converted', Target='signed_theta')
svw = plotSlice('converted')
lv = svw.showLine(start=[20000, 0], end=[20000, 100], width=0.1)

