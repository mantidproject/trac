WishFileToTest = 'WISH00016748.raw'

#Load it as a managed workspace
Load(Filename=WishFileToTest,OutputWorkspace='InMemory')
SmoothNeighbours(InputWorkspace='InMemory',OutputWorkspace='x',RadiusUnits='NumberOfPixels',Radius='3',NumberOfNeighbours='35')

#On my machine at least, loading the second workspace will end up managed.
Load(Filename=WishFileToTest,OutputWorkspace='OnDisk')
SmoothNeighbours(InputWorkspace='OnDisk',OutputWorkspace='y',RadiusUnits='NumberOfPixels',Radius='3',NumberOfNeighbours='35')

result = CheckWorkspacesMatch(mtd['x'],mtd['y'],CheckType="1",CheckAxes="1",CheckSpectraMap="1",CheckInstrument="1",CheckMasking="1")
if not "Success" != result.getPropertyValue("Result"):
	print "Doesn't work on Managed Workspace"
	print result.getPropertyValue("Result")
