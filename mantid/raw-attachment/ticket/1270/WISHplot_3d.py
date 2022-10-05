# Creates a mayavi 3D  plot from a WISH Nexus Processed File (ie useable for small machines)
# It therefore assumes the data is already transformed in q or in lambda 
import matplotlib.pyplot as p
import numpy as np
from scipy import *
from pylab import *
from math import atan2, degrees
#from scipy.optimize import leastsq
#import sys
#sys.path.append('/opt/lib/python2.4/site-packages/enthought.tvtk-2.0.2.dev_r18171-py2.4-linux-x86_64.egg/enthought/')
from enthought.mayavi import mlab
from enthought.tvtk.api import tvtk
from enthought.mayavi.scripts import mayavi2
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.mayavi.modules.surface import Surface
pi=np.pi

def cart2sph(x,y,z):
  r=(x**2+y**2+z**2)**0.5
  theta=atan2(y,x)
  phi=atan2(z,(x**2+y**2)**0.5)
  return r,theta,phi

def sph2cart(r,theta,phi):
  x=r*sin(theta)*cos(phi)
  y=r*sin(theta)*sin(phi)
  z=r*cos(theta)
  return x,y,z

def make_3dgrid(x,y,z,s):
	print "making a 3D grid..."
	sx=int(np.size(x)/256.0)
	sy=int(np.size(y)/256.0)
	sz=int(np.size(z)/256.0)
	bigx=np.zeros([sx,sy,sz])
	bigy=np.zeros([sx,sy,sz])
	bigz=np.zeros([sx,sy,sz])
	bigs=np.zeros([sx,sy,sz])
	for i in range(0,sx):
		bigx[i,:,:]=x[i]
	for j in range(0,sy):
		bigy[:,j,:]=y[j]
	for k in range(0,sz):
		bigz[:,:,k]=z[k]
		bigs[k,k,k]=s[k]
	return bigx,bigy,bigz,bigs

def make_squares(nbpanels,nbtubesperpanel,nbpixelspertube):
  squares=np.zeros( ( nbpanels*(nbtubesperpanel-1)*(nbpixelspertube-1) ,4 ),'int')
  spectrum=0
  for h in range(0,nbpanels):
    for i in range(0,nbtubesperpanel-1):
      for j in range(0,nbpixelspertube-1):
	  squares[spectrum,0]=j+nbpixelspertube*(i+h*nbtubesperpanel)
	  squares[spectrum,1]=j+nbpixelspertube*(i+h*nbtubesperpanel)+1
	  squares[spectrum,2]=j+nbpixelspertube*(i+1+h*nbtubesperpanel)+1
	  squares[spectrum,3]=j+nbpixelspertube*(i+1+h*nbtubesperpanel)
	  spectrum+=1
  return squares

def get_size_wksp(work_handle):
  return work_handle.getNumberHistograms()

def get_info_source_sample(work_handle):
  print "getting info from instrument"
  sample=work_handle.getInstrument().getSample()
  source=work_handle.getInstrument().getSource()
  samplePos=sample.getPos()
  beamPos=samplePos-source.getPos()
  return sample,samplePos,beamPos

def get_spectrum_x_y(work_handle,spectrum_number):
  x=work_handle.readX(spectrum_number)[0]
  y=work_handle.readY(spectrum_number)[0]
  return x,y

def get_r_twotheta_phi_detector(work_handle,spectrum_number,s,sp,bp):
  udet=work_handle.getDetector(spectrum_number)
  r=udet.getDistance(s)
  twotheta=udet.getTwoTheta(sp,bp)
  phi=udet.getPhi()
  return r,twotheta, phi

def create_map_single_nxs(wname):
  try:
    h=mantid.getMatrixWorkspace(wname)
  except:
    print "Could not find workspace"+wname
  sizew=get_size_wksp(h)
  datax=n.zeros(sizew)
  print datax
  datay=n.zeros(sizew)
  dataz=n.zeros(sizew)
  datas=n.zeros(sizew)
  print "nb of histograms "+str(sizew)
  s,sp,bp=get_info_source_sample(h)
  for spectrum_number in range(0,sizew):
    x,y=get_spectrum_x_y(h,spectrum_number)
    r,t,p=get_r_twotheta_phi_detector(h,spectrum_number,s,sp,bp)
    oneoverx=1.0/x
    datax[spectrum_number],datay[spectrum_number],dataz[spectrum_number]=sph2cart(oneoverx,t,p)
    datas[spectrum_number]=y
  return datax,datay,dataz,datas

def plot_map(x,y,z,s):
  src=mlab.pipeline.scalar_field(x,y,z,s)
  mlab.pipeline.image_plane_widget(src,plane_orientation='z_axes',slice_index=10,opacity=0.3)
  mlab.pipeline.volume(src)
  return
  

def make_Laue_map(wname):
  nbmonitors=5
  work_handle=mantid.getMatrixWorkspace(wname)
  wsize=get_size_wksp(work_handle)
  max=int(1.0*wsize)-nbmonitors
  s=np.zeros(max)
  xyz=np.zeros((max,3))
  for spectrum in range (0,max):
    s[spectrum]=work_handle.readY(spectrum+nbmonitors)[0]
    pos=work_handle.getDetector(spectrum+nbmonitors).getPos()
    xyz[spectrum,0]=pos.getX()
    xyz[spectrum,1]=pos.getY()
    xyz[spectrum,2]=pos.getZ()
  return xyz,s

def create_tvtk_mesh(points,squares,valuestoplot):
    print "making the polys"
    mesh = tvtk.PolyData(points=points, polys=squares)
    print "making the scalar"
    mesh.point_data.scalars = valuestoplot
    mesh.point_data.scalars.name = 'IntegratedIntensity'
    return mesh
#@mlab.show
def Laue_plot(mesh,vmin,vmax):
    print "making the engine"
    engine = mlab.get_engine()
    #replacemlab.figure(1) by mlab.figure() and comment malb.clf() to create a new figure each time
    fig = mlab.figure()
    #mlab.clf()
    #bgcolor=(0, 0, 0), fgcolor=(0, 0, 0), figure=mesh.class_name[3:])
    print "calling VTKDataSource"
    src = VTKDataSource(data=mesh)
    print "add source to engine"
    engine.add_source(src) 
    print "calling pipeline.surface"
    mlab.pipeline.surface(src, opacity=1.0,vmin=vmin,vmax=vmax)        
    #mlab.pipeline.surface(mlab.pipeline.extract_edges(src),
    #                        color=(0, 0, 0), )
    a=fig.scene
    return a

LoadNexusProcessed("w3319.nx5","w3319")
print "making the map"
xyz,integratedint=make_Laue_map("w3319")
print "map made, now making squares"
sq=make_squares(5,152,128)
print "squares made, now making tvtk mesh"
mesh=create_tvtk_mesh(xyz,sq,integratedint)
print "tvtk mesh made, now making the plot"   
a=Laue_plot(mesh,0,2000)



========================================================
def picker_callback(picker_obj, evt):
    picker_obj = tvtk.to_tvtk(picker_obj)
    picked = picker_obj.actors
    if mesh.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
        # m.mlab_source.points is the points array underlying the vtk
        # dataset. GetPointId return the index in this array.
        x_, y_ = np.lib.index_tricks.unravel_index(picker_obj.point_id,
                                                                r.shape)
        print "Data indices: %i, %i" % (x_, y_)
        n_x, n_y = r.shape
        cursor.mlab_source.set(x=np.atleast_1d(x_) - n_x/2., 
                               y=np.atleast_1d(y_) - n_y/2.)
        cursor3d.mlab_source.set(x=np.atleast_1d(x[x_, y_]), 
                                 y=np.atleast_1d(y[x_, y_]),
                                 z=np.atleast_1d(z[x_, y_]))
        #x_, y_, z_ = picker_obj.pick_position
        #cursor3d.mlab_source.set(x=np.atleast_1d(x_),
        #                         y=np.atleast_1d(y_),
        #                         z=np.atleast_1d(z_))

a.picker.pointpicker.add_observer('EndPickEvent', picker_callback)

################################################################################
# Some logic to pick on click but no move
class MvtPicker(object):
    mouse_mvt = False

    def __init__(self, picker):
        self.picker = picker

    def on_button_press(self, obj, evt):
        self.mouse_mvt = False

    def on_mouse_move(self, obj, evt):
        self.mouse_mvt = True

    def on_button_release(self, obj, evt):
        if not self.mouse_mvt:
            x, y = obj.GetEventPosition()
            self.picker.pick((x, y, 0), fig.scene.renderer)
        self.mouse_mvt = False
        


mvt_picker = MvtPicker(a.picker.pointpicker)

a.interactor.add_observer('LeftButtonPressEvent', 
                                mvt_picker.on_button_press)
a.interactor.add_observer('MouseMoveEvent', 
                                mvt_picker.on_mouse_move)
a.interactor.add_observer('LeftButtonReleaseEvent', 
                                mvt_picker.on_button_release)


mlab.show()

def test_getdetectorinfo(wname,spectrumnumber):
  h=mantid.getMatrixWorkspace(wname)
  s,sp,bp=get_info_source_sample(h)
  r,t,p=get_r_twotheta_phi_detector(h,spectrumnumber,s,sp,bp)
  print r, degrees(t), degrees(p)
  return

#test_getdetectorinfo("w3319_1",1000)
#ewald=create_map_single_nxs("w3319_1")
#plot_map(ewald)

#x,y,z,s=create_map_single_nxs("w3319")
#print "data created. Now trying to plot"
#bigx,bigy,bigz,bigs=make_3dgrid(x,y,z,s)
#print "grid made"
#plot_map(bigx,bigy,bigz,bigs)
