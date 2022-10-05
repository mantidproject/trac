################################################################################
#
# Import PDFgetN data
#
################################################################################

def parseIDLData(filename):
    """ Parse PDFgetN data file

    Return:
     - List of tuple
        - x_array
        - y_array
        - e_array
    """
    import math
    print "Parsing IDL File %s" % (filename)

    # 1. Open file
    manfile = open(filename, "r")
    lines = manfile.readlines()
    manfile.close()

    # 2. Parse
    xl = []
    yl = []
    el = []

    xlargestnan = -1.0E10
    
    for lindex in xrange(0, len(lines)):
        line = lines[lindex].strip()

        if line == "":
            # a) Empty line
            pass
        
        elif line.startswith("#"):
            # b) #-line: pass
            pass

        else:
            # c) Data line
            line = line.lower() 
            terms = line.split()
            if line.count("n") > 0 or line.count("i"):
                # NAN or Infty: Special treat
                x = float(terms[0])
                y = 0.0
                e = 1.0E5

                if x > xlargestnan:
                    xlargestnan = x

            else:
                # regular data-line
                x = float(terms[0])
                y = float(terms[1])
                e = math.sqrt(abs(y))
            # END-IF
            xl.append(x)
            yl.append(y)
            el.append(e)

        # END-IF
    # END-FOR

    dataset = (xl, yl, el)

    print "Data File %s Range = (%f, ...)" %  (filename, xlargestnan)

    return dataset


def revertArray(a):
    """ Revert order of arrays
    """
    aa = []
    for ai in xrange(len(a)):
        item = a[ai]
        aa.insert(0, item)

    return aa


def main(argv, unit):
    """ Main method:  Import a series of file 
    """
    # 1. Parse args
    filenames = []
    for iarg in xrange(1, len(argv)):
        filename = argv[iarg]
        filenames.append(filename)

    # 2. Generate Workspace
    for filename in filenames:
        # 2.1 Parse data file
        dataset = parseIDLData(filename)
        x = dataset[0]
        y = dataset[1]
        e = dataset[2]

        # 2.2 in right order
        if x[1] < x[0]:
            x = revertArray(x)
            y = revertArray(y)
            e = revertArray(e)
        # ENDIF

        # 2.3 Create Workspace
        wsname = filename.split("/")[-1].split('.')[0]
        CreateWorkspace(wsname, x, y, e, 1, unit)
    # END-FOR

    return


if __name__=="__main__":
    argv = ["x",
            "./IDLData/nom1818bank0.dat",
            "./IDLData/nom1818bank1.dat",
            "./IDLData/nom1818bank2.dat",
            "./IDLData/nom1818bank3.dat",
            "./IDLData/nom1818bank4.dat",
            "./IDLData/nom1818bank5.dat",
            ]
    unit = "MomentumTransfer"
    argv = ["x",
            "./NOM_1818ftf.gr"
            ]
    unit = ""
    main(argv, unit)
