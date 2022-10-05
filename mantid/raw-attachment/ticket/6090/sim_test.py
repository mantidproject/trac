config['default.facility']="SNS"

ws_name = "ARCS_sim_event_spe"
ei_guess = 1000.0

ws = DgsReduction(
                  SampleInputFile="ARCS_sim_event.nxs",
                  OutputWorkspace=ws_name,
                  IncidentEnergyGuess=ei_guess,
                  UseIncidentEnergyGuess=True,
                  IncidentBeamNormalisation="None",
                 )

sws = SumSpectra(ws[0], OutputWorkspace=ws_name+"_s")
plt1 = plotSpectrum(sws, 0)

sqw_ws = SofQW(ws[0], OutputWorkspace=ws_name+"_sqw", QAxisBinning="13,0.05,15", 
               EMode="Direct", EFixed=ei_guess)
plt2 = plotSlice(sqw_ws)
