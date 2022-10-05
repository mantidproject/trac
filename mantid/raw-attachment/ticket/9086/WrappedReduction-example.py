from WrappedReduction import *

#####################        M2-0167 T=5K 
#( _ ,r1q , _)= ref('8169+8171+8173+8175+8177+8179+8181',theta=0.4)  #Test ref()
#r1q= refl('8169+8171+8173+8175+8177+8179+8181',theta=0.4)  # Test refl
r1q= refq('8169+8171+8173+8175+8177+8179+8181',theta=0.4)  # Test refq

graph0=plotSpectrum(r1q,0); 
graph0.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph0.activeLayer().setAutoScale();

#(_ ,r2q,  _)= ref('8197+8198+8199+8200', 0.615)
#r2q= refl('8197+8198+8199+8200', 0.615)
r2q= refq('8197+8198+8199+8200', 0.615)

graph0=plotSpectrum(r2q,0); 
graph0.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph0.activeLayer().setAutoScale();

#( _ ,r3q , _)= ref('8170+8172+8174+8176+8178+8180', theta=1.52)
#r3q= refl('8170+8172+8174+8176+8178+8180', theta=1.52)
r3q= refq('8170+8172+8174+8176+8178+8180', theta=1.52)

graph0=plotSpectrum(r3q,0); 
graph0.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph0.activeLayer().setAutoScale();

# Plot the data to check the results
graph0=plotSpectrum([r1q,r2q,r3q],0); 
graph0.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph0.activeLayer().setAutoScale();

# Rebin prior to stitching
rr1q=Rebin(r1q,'0.009,-0.02,0.048')
rr2q=Rebin(r2q,'0.014,-0.02,0.066')
rr3q=Rebin(r3q,'0.026,-0.02,0.18')

# Plot the data to check the results
graph1=plotSpectrum([rr1q,rr2q,rr3q],0); 
graph1.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph1.activeLayer().setAutoScale();
### Test Matplotlib graphics
plt.plot(centerbins(rr1q[0].readX(0)),rr1q[0].readY(0), 'r.-',centerbins(rr1q[1].readX(0)),rr1q[1].readY(0), 'k.-' )
plt.plot(centerbins(rr2q[0].readX(0)),rr2q[0].readY(0), 'b.-',centerbins(rr2q[1].readX(0)),rr2q[1].readY(0), 'g.-' )
plt.plot(centerbins(rr3q[0].readX(0)),rr3q[0].readY(0), 'c.-',centerbins(rr3q[1].readX(0)),rr3q[1].readY(0), 'm.-' )
#plt.show()   # Causes a full mantid crash.

"""
# Stitch three data sets together 
r5k = Stitch1DMany([rr1q,rr2q,rr3q], [0.014,0.026],[0.048,0.066],-0.05)

# Plot the stitched data
graph2=plotSpectrum(r5k,0); 
graph2.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph2.activeLayer().setAutoScale();
# Normalize the area of total reflection to 1
y0=r5k[0].readY(0); y1=r5k[1].readY(0); 
avg=numpy.average( numpy.array( ( numpy.average(y0[0:10]), numpy.average(y1[0:10]) ) ) )
r5k=r5k/avg

# Write out textfiles
#SaveAscii(r5k[0],'M2-167T=5KH=0p9T.001.dat', ScientificFormat=True,ColumnHeader=False)
#SaveAscii(r5k[1],'M2-167T=5KH=0p9T.002.dat', ScientificFormat=True,ColumnHeader=False)

#calculate the spin asymmetry and flipping ratio.  We rebin again to improve the error bar on the high q data
rr=Rebin(r5k,'0.009,-0.05,0.02,0.07,0.2')
asym=(rr[0]-rr[1])/(rr[0]+rr[1])
ratio=rr[0]/rr[1]

# Plot the stitched data
graph3=plotSpectrum(asym,0);  graph3.activeLayer().setAxisTitle(0, "SA")
graph4=plotSpectrum(Ratio,0);  graph4.activeLayer().setAxisTitle(0, "Ratio")
g=mergePlots(graph3,graph4)

# Write out textfiles
#SaveAscii(asym,'M2-167T=5KH=0p9T.asy.dat', ScientificFormat=True,ColumnHeader=False)
#SaveAscii(ratio,  'M2-167T=5KH=0p9T.rat.dat', ScientificFormat=True,ColumnHeader=False)

"""
'''
#################################################################################################
#####################        M2-0167 T=50K 
#################################################################################################
r1q = refq('8187+8189+8191+8193', theta=0.401)
r2q = refq('8196', theta=0.61)
r3q = refq('8195', theta=0.9)
r4q = refq('8188+8190+8192+8194', theta=1.501)
# Rebin prior to stitching
rr1q=Rebin(r1q,'0.009,-0.02,0.048')
rr2q=Rebin(r2q,'0.0155,-0.02,0.06')
rr3q=Rebin(r3q,'0.018,-0.02,0.1')
rr4q=Rebin(r4q,'0.026,-0.02,0.2')

# Plot the data to check the results
graph1=plotSpectrum([rr1q,rr2q,rr3q,rr4q],0); 
graph1.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph1.activeLayer().setAutoScale();

# Stitch three data sets together
r50k = Stitch1DMany([rr1q,rr2q,rr3q,rr4q], [0.0155,0.18,0.026],[0.048,0.06,0.1],'-0.05')

# Plot the stitched data
graph2=plotSpectrum(r50k,0); 
graph2.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph2.activeLayer().setAutoScale();
# Normalize the area of total reflection to 1
y0=r50k[0].readY(0); y1=r50k[1].readY(0); 
avg=numpy.average( numpy.array( ( numpy.average(y0[0:10]), numpy.average(y1[0:10]) ) ) )
r50k=r50k/avg

# Write out textfiles
#SaveAscii(r5k[0],'M2-167T=50KH=0p9T.001.dat', ScientificFormat=True,ColumnHeader=False)
#SaveAscii(r5k[1],'M2-167T=50KH=0p9T.002.dat', ScientificFormat=True,ColumnHeader=False)

 #calculate the spin asymmetry and flipping ratio.  We rebin again to improve the error bar on the high q data
rr=Rebin(r50k,'0.009,-0.05,0.02,0.07,0.2')
asym=(rr[0]-rr[1])/(rr[0]+rr[1])
ratio=rr[0]/rr[1]

# Plot the stitched data
graph3=plotSpectrum(asym,0);  graph3.activeLayer().setAxisTitle(0, "SA")
graph4=plotSpectrum(Ratio,0);  graph4.activeLayer().setAxisTitle(0, "Ratio")
g=mergePlots(graph3,graph4)

# Write out textfiles
#SaveAscii(asym,'M2-167T=50KH=0p9T.asy.dat', ScientificFormat=True,ColumnHeader=False)
#SaveAscii(ratio,  'M2-167T=50KH=0p9T.rat.dat', ScientificFormat=True,ColumnHeader=False)

#################################################################################################
#####################        M2-0167 T=300K 
#################################################################################################
r1q=refq('8209+8210+8211', theta=0.618)
r2q=refq('8212+8213+8214+8215+8216+8217+8218+8219+8220+8221+8222+8223+8224', theta=0.93)
# Rebin prior to stitching
rr1q=Rebin(r1q,'0.01,-0.03,0.048')
rr2q=Rebin(r2q,'0.018,-0.03,0.15')

# Plot the data to check the results
graph1=plotSpectrum([rr1q,rr2q],0); graph1.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph1.activeLayer().setAutoScale();

# Stitch three data sets together
r300k = Stitch1DMany([rr1q,rr2q], [0.018],[0.048],'-0.05')

# Plot the stitched data
graph2=plotSpectrum(r300k,0);  graph2.activeLayer().setAxisScale(Layer.Left,1e-7,1,Layer.Log10); graph2.activeLayer().setAutoScale();

# Normalize the area of total reflection to 1
y0=r300k[0].readY(0); y1=r300k[1].readY(0); 
avg=numpy.average( numpy.array( ( numpy.average(y0[0:10]), numpy.average(y1[0:10]) ) ) )
r300k=r300k/avg

# Write out textfiles
#SaveAscii(r300k[0],'M2-167T=300KH=0p9T.001.dat', ScientificFormat=True,ColumnHeader=False)
#SaveAscii(r300k[1],'M2-167T=300KH=0p9T.002.dat', ScientificFormat=True,ColumnHeader=False)

#calculate the spin asymmetry and flipping ratio.  We rebin again to improve the error bar on the high q data
rr=Rebin(r300k,'0.009,-0.05,0.02,0.07,0.2')
asym=(rr[0]-rr[1])/(rr[0]+rr[1])
ratio=rr[0]/rr[1]

# Plot the stitched data
graph3=plotSpectrum(asym,0);  graph3.activeLayer().setAxisTitle(0, "SA")
graph4=plotSpectrum(Ratio,0);  graph4.activeLayer().setAxisTitle(0, "Ratio")
g=mergePlots(graph3,graph4)

# Write out textfiles
#SaveAscii(asym,'M2-167T=300KH=0p9T.asy.dat', ScientificFormat=True,ColumnHeader=False)
#SaveAscii(ratio,  'M2-167T=300KH=0p9T.rat.dat', ScientificFormat=True,ColumnHeader=False)

'''
