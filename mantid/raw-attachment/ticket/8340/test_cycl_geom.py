import IndirectAbsCor as Main

sname = 'irs26176_graphite002_red'
LoadNexusProcessed(Filename=sname, OutputWorkspace=sname)

beam = [3.0, 1.0, -1.0, 2.0, -2.0, 0.0, 3.0, 0.0, 3.0]
size = [0.2, 0.25, 0.26, 0.0]
density = [0.1, 0.1, 0.1]
sigs = [5.0, 0.1, 0.1]
siga = [0.0, 5.0, 5.0]
avar = 0.002
verbOp = True
saveOp = False
Main.AbsRun(sname, 'cyl', beam, 2, size, density,
    sigs, siga, avar, verbOp, saveOp)
    