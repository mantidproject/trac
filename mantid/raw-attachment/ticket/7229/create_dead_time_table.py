# Create a dummy dead time table, where all the dead times are 0.015
mtd.remove("dead_times")

t = WorkspaceFactory.createTable()
t.addColumn("int", "Index")
t.addColumn("double", "Value")
for i in range(0, ws.getNumberHistograms()):
	t.addRow([i + 1, 0.015])
		
mtd.add("dead_times", t)