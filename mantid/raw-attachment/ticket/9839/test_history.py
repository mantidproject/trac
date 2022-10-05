import os

Load(Filename='TSC11453.raw', OutputWorkspace='TSC11453', LoaderName='LoadRaw', LoaderVersion=3, LoadLogFiles=False)

ChopData(InputWorkspace='TSC11453', OutputWorkspace='TSC11453', IntegrationRangeLower=5000, IntegrationRangeUpper=10000, MonitorWorkspaceIndex=140)
MergeRuns(InputWorkspaces='TSC11453_1,TSC11453_2,TSC11453_3,TSC11453_4', OutputWorkspace='TSC11453_merged')

SaveNexusProcessed(InputWorkspace='TSC11453_merged', Filename='TSC11453-SNP.nxs')
SaveNexus(InputWorkspace='TSC11453_merged', Filename='TSC11453-SN.nxs')
DeleteWorkspace('TSC11453')

assert os.path.isfile('/home/chs18285/workspace/TSC11453-SN.nxs')
assert os.path.isfile('/home/chs18285/workspace/TSC11453-SNP.nxs')

