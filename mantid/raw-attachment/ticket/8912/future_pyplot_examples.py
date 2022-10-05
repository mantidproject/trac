from pymantidplot.future.pyplot import *

## plot arrays
plot([0.1, 0.3, 0.2, 4])
plot([0.1, 0.2, 0.3, 0.4], [1.2, 1.3, 0.2, 0.8])


# Loads
ws = Load("MAR11060.raw", OutputWorkspace="foo")
mar = Load('MAR11060.raw', OutputWorkspace="MAR11060")
loq=Load('LOQ48097.raw', OutputWorkspace="LOQ48097")
ws2 = Load('HRP39182.RAW', OutputWorkspace="HRP39182")

## plot workspaces
plot(ws, 100)
plot(ws, [100, 101, 102])
plot('MAR11060', [10,100,500])
plot(mar,[3, 500, 800])
yscale('log')
plot([mar, 'LOQ48097'], [800, 900])
plot([mar, loq], [800, 900])
plot(['MAR11060', loq], [800, 900])
plot(['MAR11060', loq], [800, 900], tool='plot_spectrum')

# tools
plot_spectrum(['MAR11060', loq], [800, 900])
plot(ws, [1, 5, 7, 100], tool='plot_bin')

plot_bin(ws, [1, 5, 7, 100], linewidth=4, linestyle=':')
xscale('log')

simple_md_ws = CreateMDWorkspace(Dimensions='3',Extents='0,10,0,10,0,10',Names='x,y,z',Units='m,m,m',SplitInto='5',MaxRecursionDepth='20',OutputWorkspace=MDWWorkspaceName)
plot(simple_md_ws, tool='plot_md')
plot_md(simple_md_wsws)

# some plot properties
a = [0.1, 0.3, 0.2, 4]
plot(a)
import numpy as np
y = np.sin(np.linspace(-2.28, 2.28, 1000))
plot(y, linestyle='-.', marker='o', color='red')
plot(1.5*y, '-.g', hold='on')
plot(0.8*y, ':b', hold='on')
plot(1.2*y, '--c', hold='on')
xscale('log')
yscale('log')

# plot properties and return lines
lines = plot([ws2], 0, '-r') # solid (default)
lines = plot([ws, ws2], 0, '-.c') # dash-dotted
lines = plot(ws, 0, '--m') # dashed
lines = plot(ws, [0,1], ':g')  # dotted
lines = plot(loq, [100, 104], tool='plot_spectrum', linestyle='-.', marker='*', color='red')
lines[0].get_xdata()
lines[0].get_ydata()
fig = lines[0].figure()
fig.suptitle('Example figure title')

# functions
title('Test plot of LOQ')
xlabel('ToF')
ylabel('Counts')
ylim(0, 8)
xlim(1e3, 4e4)
xscale('log')
grid('on')
savefig('example_saved_figure.png')

# hold
lines = plot(loq, [100, 102], linestyle='-.', color='red')
lines = plot(loq, 100, linestyle='-.', color='red')
lines = plot(loq, 102, linestyle='-.', color='blue', hold='on')
lines = plot(loq, 103, linestyle=':', color='m', hold='on')
lines = plot(loq, 104, linestyle=':', color='k', hold='on')

# multi-plot
plot(ws, [100, 101], 'r', ws, [200, 201], 'b', tool='plot_spectrum')
plot(ws, [100, 101], 'm', mar, [50, 41], 'b', tool='plot_spectrum')

# other examples, used to fail
ws = CreateWorkspace([1,2,3], [1.1,2.8,3.2])
lines = plot([ws], [0], '--r', [ws], [0], 'g')
lines = plot([ws], [0], 'r', [ws], [0], 'g')
title('myplot_1')
xlabel('x')
figure(0)
title('myplot_0')
xlabel('x')
print dir(lines[0])

# Axes
lines = plot(mar,[3, 500, 800])
fig = lines[0].figure()
all_ax = fig.axes()    # fig.axes() returns in principle a list
ax = all_ax[0]         #  but we only use one axes
ax.set_ylabel('--- Counts ---')
ax.set_xlabel('--- ToF ---')
ax.set_ylim(0, 25)
ax.set_xlim(1e2, 4e4)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_yscale('linear')

