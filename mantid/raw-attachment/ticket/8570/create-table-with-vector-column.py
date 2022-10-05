newTable = WorkspaceFactory.createTable()
newTable.addColumn("vector_int", "Numbers")

for i in range(1,10):
	newTable.addRow([range(0,i)])

mtd.addOrReplace("NewTable", newTable)