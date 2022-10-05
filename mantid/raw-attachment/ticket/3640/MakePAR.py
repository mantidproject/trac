import nxs
from string import join
from numpy import *

def correctangle(angle):
	angle[angle>pi]-=2*pi
	angle[angle<-pi]+=2*pi
	return angle

def MakePAR():
	filestr='CNCS_7860_event.nxs'
	fid = nxs.open(filestr,'r')
	#determine the banks in the file
	fid.openpath('/entry/instrument')
	banks=array(fid.getentries().keys())
	banks=banks[(banks>'bank')&(banks<'bank999')]
	banknums=cast['int'](join(banks).split('bank')[1:])
	banknums.sort()
	pararray=array([1,2,3,4,5,6]).reshape(6,1)
	for b in banknums:
		print b
		#get distance
		fid.openpath('/entry/instrument/bank'+str(b)+'/distance')
		dist=fid.getdata().reshape(1,-1)
		#get angles
		fid.openpath('/entry/instrument/bank'+str(b)+'/azimuthal_angle')
		azi=degrees(fid.getdata()).reshape(1,-1)
		fid.openpath('/entry/instrument/bank'+str(b)+'/polar_angle')
		pol=degrees(fid.getdata()).reshape(1,-1)
		#get x and y pixel values in bank frame
		fid.openpath('/entry/instrument/bank'+str(b)+'/x_pixel_offset')
		xc=fid.getdata().reshape(1,-1)
		fid.openpath('/entry/instrument/bank'+str(b)+'/y_pixel_offset')
		yc=fid.getdata().reshape(1,-1)
		fid.openpath('/entry/instrument/bank'+str(b)+'/pixel_id')
		pid=fid.getdata().reshape(1,-1)
		#get xw yw
		fid.openpath('/entry/instrument/bank'+str(b))
		k=fid.getentries().keys()
		if 'x_pixel_size' in k: 
			fid.openpath('/entry/instrument/bank'+str(b)+'/x_pixel_size')
			xw=fid.getdata().reshape(1,-1)
		else:
			xw=xc[0,1]-xc[0,0]
		if 'y_pixel_size' in k: 
			fid.openpath('/entry/instrument/bank'+str(b)+'/y_pixel_size')
			yw=fid.getdata().reshape(1,-1)
		else:
			yw=yc[0,1]-yc[0,0]
		#add information to the par file
		pararray=append(pararray,concatenate((dist,pol,azi,dist*0.+xw,dist*0+yw,pid)),axis=1)

	#get rid of the first line of the pararray
	pararray=pararray[:,1:].T
	#write it to a file
	f=open('SEQ-new.par','w')
	x,y=pararray.shape
	formatStr = " %0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%d"
	print >>f, x
	for i in range(x):
		print >>f,formatStr % (pararray[i,0],pararray[i,1],pararray[i,2],pararray[i,3],pararray[i,4],pararray[i,5])
	f.close()

if __name__=="__main__":
	MakePAR()



