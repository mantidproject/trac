applyDeadTimeCorr = False

prefix = "/home/hgb24396/Mantid/Develop/Source/Test/AutoTestData/MUSR000"

start =  15189
end = 15199

result = WorkspaceFactory.create("Workspace2D", 1, end - start + 1, end - start + 1)

mtd.remove("script_result")
mtd.add("script_result", result)

for run_no in range(start,end+1):
	# Load the file
	file = prefix + str(run_no) + ".nxs"
	loaded = LoadMuonNexus(file, AutoGroup=False)

	# Apply dead time correction
	if applyDeadTimeCorr:
		loaded = ApplyDeadTimeCorr("loaded", "dead_times")
	
	# Apply auto-grouping
	loaded = ApplyGroupingFromMuonNexus("loaded", file)
	
	# Integrate the values
	loaded = Integration("loaded")
	
	# Calculate and print assymetry
	loaded = AsymmetryCalc("loaded")
	
	# Get first period
	first = loaded.getItem(0)
	
	# Set result value
	result.dataY(0)[run_no - start] = first.readY(0)[0]
	result.dataX(0)[run_no - start] = run_no