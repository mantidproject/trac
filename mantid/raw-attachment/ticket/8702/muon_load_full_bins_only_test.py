rebin_fixed_params = 2.0 # bin size of 0.016 * 2
finish = 10.0	

emu_loaded_tuple = LoadMuonNexus("emu00006473.nxs", DetectorGroupingTable="emu_grouping")
emu_loaded = emu_loaded_tuple[0]

rebin_params = (emu_loaded.readX(0)[1] - emu_loaded.readX(0)[0]) * rebin_fixed_params

result = MuonLoad("emu0006473.nxs", "emu_grouping", RebinParams=str(rebin_params), OutputType="GroupCounts", GroupIndex=0)