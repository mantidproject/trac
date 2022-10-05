#Corr
import CorrTestFirst as Main


def CorrBegin(prog,sname,cname):
	geom = 'Cyl'
	ana = 'graphite004'
	ncan = 2
	Main.CorrStart(prog,ncan,ana,sname,cname,geom)
	

prog = 'Correct'
sname = 'osi92711'
cname = 'osi92756'
CorrBegin(prog,sname,cname)
ns = 0
res = sname +'_'+ prog +'_' + cname[3:8]
plotSpectrum([sname,cname,res],ns)	
