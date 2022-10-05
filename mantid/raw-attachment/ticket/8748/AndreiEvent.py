import numpy as np
# make these smaller to increase the resolution
dx, dy = 0.1, 0.1

# generate 2 2d grids for the x & y bounds
y, x = np.mgrid[slice(3, 7 + dy, dy),
                slice(3, 7 + dx, dx)]

z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)


z=(z*5+5).astype(int)
z[np.where(z<0)]=0

location = "/Users/spu92482/Desktop/AndreiEvents.txt"
f1=open(location,"w")
f1.write("DIMENSIONS\n")
f1.write("Qx Qx rlu 40\n")
f1.write("Qy Qy rlu 40\n")
f1.write("MDEVENTS\n")
#f1.write("#")
for i in range(41):
    for j in range(41):
        for ev in range(int(z[i][j])):
            f1.write("1.\t1.\t"+str(x[i][j]-3)+"\t"+str(y[i][j]-3)+"\n")
f1.close()

mdws =ImportMDEventWorkspace(Filename=location)