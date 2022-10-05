data = [[1,2,3,4,5],
             [1,2,3,4,5],
	     [2,4,8,16,32]]
	     
t = newTable("TestTable2", len(data[0]), len(data))

for colNum, row in enumerate(data):
	for rowNum, element in enumerate(row):
		t.setCell(colNum + 1, rowNum + 1, element)