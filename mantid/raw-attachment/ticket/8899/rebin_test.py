import math
import numpy as np

ws = WorkspaceFactory.create("Workspace2D", 1, 10, 9)

ws.setX(0, np.array([0.5,1.25,2,2.75,3.5, 4.25, 5, 5.75, 6.5, 7.25]))

yVal = np.empty(9); yVal.fill(3.0)
ws.setY(0, yVal)

eVal = np.empty(9); eVal.fill( math.sqrt(3.0) )
ws.setE(0, eVal)

mtd.addOrReplace("ws", ws)
mtd.addOrReplace("ws", ws) # That works fine

binnedWs = Rebin(ws, "2.0") # binnedWs is added to the ADS
mtd.addOrReplace("binnedWs", binnedWs) # Crashes here