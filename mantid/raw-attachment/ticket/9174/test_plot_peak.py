import numpy as np

ws_name = 'irs26176_graphite002_red'
res_ws_name = 'irs26173_graphite002_red'

Load(ws_name+".nxs", OutputWorkspace=ws_name)
Load(res_ws_name+".nxs", OutputWorkspace=res_ws_name)

func_string = ''
func_string  += 'name=LinearBackground,A0=0,A1=0,ties=(A0=0.000000,A1=0.0);'
func_string += '(composite=Convolution,FixResolution=true,NumDeriv=true;'
func_string += 'name=Resolution,Workspace=%s,WorkspaceIndex=0;' % res_ws_name
func_string += 'name=Lorentzian,Amplitude=1.0,PeakCentre=0.0,FWHM=0.022;'
func_string += ');'

print func_string

PlotPeakByLogValue(Input=ws_name+",v3:43", Function=func_string, CreateOutput=True, OutputCompositeMembers=True, ConvolveMembers=True, OutputWorkspace="Test")