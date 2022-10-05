Load(Filename='/home/chs18285/git/systemtests/Data/INTER00013460.nxs', OutputWorkspace='INTER00013460', LoaderName='LoadISISNexus', LoaderVersion=2)
Load(Filename='/home/chs18285/git/systemtests/Data/INTER00007709.nxs', OutputWorkspace='INTER00007709', LoaderName='LoadISISNexus', LoaderVersion=2)
ReflectometryReductionOneAuto(InputWorkspace='INTER00013460', FirstTransmissionRun='INTER00007709', OutputWorkspace='Test', OutputWorkspaceWavelength='TestWave', ThetaOut=0.70969419753330121)
