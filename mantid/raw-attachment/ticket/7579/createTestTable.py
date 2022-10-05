data = [[-1,-2,-3,-4,-5],
             [1,2,3,4,5],
	     [2,4,8,16,32],
	     [1,1,1,1,1],
	     [2,2,2,2,2],
	     [100,200,300,400,500]]
	    
columnRoles = [_qti.Table.X, _qti.Table.X, _qti.Table.Y, _qti.Table.xErr, _qti.Table.yErr, _qti.Table.Label]
	     
t = newTable("TestTable2", len(data[0]), len(data))

for colNum, row in enumerate(data):
	t.setColumnRole(colNum + 1, columnRoles[colNum])
	for rowNum, element in enumerate(row):
		t.setCell(colNum + 1, rowNum + 1, element)