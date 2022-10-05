tof_counts = Load("emu00006473.nxs")
tof_counts2 = Load("emu00006475.nxs", EntryNumber=1)

tof_myunits = CloneWorkspace("tof_counts")
tof_myunits.setYUnit("MyUnit")

dspacing_counts = Load("PG3_733.nxs")