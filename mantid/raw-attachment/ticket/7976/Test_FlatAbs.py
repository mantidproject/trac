import IndirectAbsCor as Main

sname = 'irs26176_graphite002_red'
LoadNexusProcessed(Filename=sname, OutputWorkspace=sname)

beam = ''
size = [0.1, 0.01, 0.01]
density = [0.1, 0.1, 0.1]
sigs = [5.0, 0.1, 0.1]
siga = [0.0, 5.0, 5.0]
avar = 45.0
verbOp = True
saveOp = False
Main.AbsRun(sname, 'flt', beam, 2, size, density,
    sigs, siga, avar, verbOp, saveOp)