from mantid.kernel import *
from mantid.api import *

# Author: E. Farhi  <farhi@ill.fr>
# Date:   June 19th 2014
# Description: IDF to PLY/OFF converter
 
class IDF_to_PLY(PythonAlgorithm):

    def category(self):
        return 'Utilities'

    def PyInit(self):
        # Declare properties
        self.declareProperty(FileProperty(name="InputFile",defaultValue="",
                                action=FileAction.Load, extensions = ["xml","hdf","nxs"]), 
                                doc="An input file with associated instrument definition (IDF/XML in MANTIDPATH/instrument, NeXus or HDF)")
       
        # output direction specified explicitly
        self.declareProperty(FileProperty(name="OutputFile",defaultValue="instrument_Description",
                                action=FileAction.Save, extensions = ["off","ply"]), 
            doc="The output file name where the geometry will be saved")

        # the type of Data File generated
        self.declareProperty("OutputFormat","OFF", StringListValidator(["OFF","PLY"]))

    def PyExec(self):
        # Run the algorithm

        # Load the Instrument Definition File (IDF) e.g. XML or from NXS
        ws = Load(Filename=self.getPropertyValue("InputFile"))
        
        inst  = ws.getInstrument()
        
        nhist = ws.getNumberHistograms()

        self.log().information( "IDF_to_PLY: Opening instrument " + inst.getName() + " definition from file " + self.getPropertyValue("InputFile") + " with " + str(nhist) + " pixels.")

	name = self.getPropertyValue("OutputFile")
        fid = open(name, "w")

        self.log().information( "IDF_to_PLY: Generating output file " + self.getPropertyValue("OutputFile") )

        # Mantid::Geometry::OCGeometryGenerator 
        # methods: getNumberOfPoints, getNumberOfTriangles, getTriangleFaces, getTriangleVertices

        nb_vertices = 0
        nb_polygons = 0
        vout = ""
        pout = ""

        # traverse all detector pixels
        for i in range(nhist):
            det = ws.getDetector(i);
            if not det.isMonitor():
              # det.getPos() is the position of the detector object, whatever be its internal shape and definition of origin
              # we thus prefer to use the shape and its bounding box

                BBox = det.shape().getBoundingBox() # use .centrePoint() and .width() which are V3D objects
                # create a cuboid from the boundingBox. centerPoint is really at the center of the max-min
                # so we add the +/- width/2
                pos = BBox.centrePoint() -  inst.getSample().getPos()     # shift from sample
                x0 = pos.X()
                y0 = pos.Y()
                z0 = pos.Z()
                dx = BBox.width().X()/2.0
                dy = BBox.width().Y()/2.0
                dz = BBox.width().Z()/2.0

                i = nb_vertices   # offset for vertices index

                # write the X Y Z coordinate of Detector BBox position wrt sample
                vout += '%g %g %g\n' % (x0+dx, y0-dy, z0-dz)
                vout += '%g %g %g\n' % (x0-dx, y0+dy, z0-dz)
                vout += '%g %g %g\n' % (x0-dx, y0-dy, z0+dz)
                vout += '%g %g %g\n' % (x0-dx, y0-dy, z0-dz)
                vout += '%g %g %g\n' % (x0+dx, y0-dy, z0+dz)
                vout += '%g %g %g\n' % (x0+dx, y0+dy, z0-dz)
                vout += '%g %g %g\n' % (x0+dx, y0+dy, z0+dz)
                vout += '%g %g %g\n' % (x0-dx, y0+dy, z0+dz)
                nb_vertices += 8

                # write the connections after the vertices
                pout += '%i %i %i %i %i\n' % (4, 0+i, 5+i, 6+i, 4+i)
                pout += '%i %i %i %i %i\n' % (4, 1+i, 5+i, 6+i, 7+i)
                pout += '%i %i %i %i %i\n' % (4, 2+i, 4+i, 6+i, 7+i)
                pout += '%i %i %i %i %i\n' % (4, 3+i, 0+i, 4+i, 2+i)
                pout += '%i %i %i %i %i\n' % (4, 3+i, 0+i, 5+i, 1+i)
                pout += '%i %i %i %i %i\n' % (4, 3+i, 1+i, 7+i, 2+i)
                nb_polygons += 6

        # get the file type to export, write the file content
        if self.getPropertyValue("InputFile") == 'OFF':
            fid.write("OFF\n")  # 1st line, mandatory
            fid.write("# This is an Object File Format (geomview). Use e.g. Meshlab to view it.\n")
            fid.write("# nb points, nb faces, void\n")
            fid.write("# List point coordinates\n")
            fid.write("%i %i 0\n" % (nb_vertices,nb_polygons))       # nb points, nb faces, void
            fid.write(vout)
            fid.write("# List faces, all rectangular\n")
            fid.write(pout)
        else:
            fid.write("ply\n")
            fid.write("format ascii 1.0\n")
            fid.write("comment " + inst.getName() + " geometry (Mantid IDF) from file " + self.getPropertyValue("InputFile") + "\n")
            fid.write("comment This is an PLY File Format. Use e.g. Meshlab to view it.\n")
            fid.write("element vertex %i\n" % (nb_vertices))
            fid.write("property float32 x\n")
            fid.write("property float32 y\n")
            fid.write("property float32 z\n")
            fid.write("element face %i\n" % (nb_polygons))
            fid.write("property list uint8 int32 vertex_indices\n")
            fid.write("end_header\n")
            fid.write(vout)
            fid.write(pout)
              
        self.log().information( "IDF_to_PLY: " + inst.getName() + " written to " + self.getPropertyValue("OutputFile") + " with %i vertices and %i polygons" % (nb_vertices, nb_polygons) )
        #deleteWorkspace(ws) 
	# The above line deletes is supposed to delete the workspace, however causes the Algorithm to crash, so it has been commented out.
	
# Register algorithm with Mantid
AlgorithmFactory.subscribe(IDF_to_PLY)
