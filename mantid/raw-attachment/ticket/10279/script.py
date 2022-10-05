'''Load S(E) and clone to a slightly sifted workspace. Then,
fit both workspaces and check that the Centre parameter is (close to) the 
imposed shift 0.0002
'''
q300=LoadNexus(Filename='/tmp/q300.nxs')
trial=CloneWorkspace(q300)
trial=ScaleX(trial,Factor=0.0002,Operation='Add')
fitstring='name=TabulatedFunction,Workspace=trial,WorkspaceIndex=0,Scaling=1.0,Centre=0.0'
Fit(fitstring,InputWorkspace=q300, CreateOutput=1)
