import numpy as np

ws = WorkspaceFactory.create("Workspace2D", 1, 10, 9)

xValues = np.array(range(1,11)) * 0.5 # 0.5 1.0 1.5 2.0 2.5 ...
yValues = np.empty(9); yValues.fill(3.0) # 3.0 3.0 3.0 ....

ws.setX(0, xValues)
ws.setY(0, yValues)

mtd.addOrReplace("ws", ws)

result = Rebin("ws", "0.5,2.0,5.0", FullBinsOnly=True)
# result = Rebin("ws", "0.5,2.0,5.0") - this would include the smaller last bin

