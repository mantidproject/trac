# set MANTID to SANS2D instrument, and add cycle_12_3 to the path to search

#Load the event data
run_num = 16183#16187
ws_e, mon = Load(str(run_num),LoadMonitors=True)
print ws_e.getNumberHistograms()/2 -1
ws_e = CropWorkspace(ws_e,StartWorkspaceIndex=0,EndWorkspaceIndex=ws_e.getNumberHistograms()/2-1)

# get the binning from the monitor
monitors = mon.readX(0)
step = 0
values = []
for i in range(len(monitors)-1):
	if monitors[i+1] - monitors[i] == step: continue
        values.append(monitors[i])
        step = monitors[i+1] - monitors[i]
        values.append(step)

values.append(monitors[-1])

# rebin the event data to produce histograms
hist = Rebin(ws_e, Params=values, PreserveEvents=False)

# concatenate the monitor and the histogram. You will end up with
# the workspace: ws_e_monitors. 
# ShowInstrument in this workspace and you will see only a blank detectors
ConjoinWorkspaces(mon, hist)


# I was expecting something like this one.
hist_ws = LoadNexus(str(run_num))

CheckWorkspacesMatch('ws_e_monitors','hist_ws')