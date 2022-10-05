def furyfitSeq(inputWS, func, ftype, startx, endx, Save, Plot, Verbose=True):
    StartTime('FuryFit Mult')
    workdir = config['defaultsave.directory']
    option = ftype[:-2]
    if Verbose:
        logger.notice('Option: '+option)  
    input = inputWS+',i0'
    nHist = mtd[inputWS].getNumberHistograms()
    for i in range(1,nHist):
        input += ';'+inputWS+',i'+str(i)
    outNm = getWSprefix(inputWS) + 'fury'
    f1 = """(
        composite=CompositeFunctionMW,Workspace=$WORKSPACE$,WSParam=(WorkspaceIndex=$INDEX$);
        name=LinearBackground,A0=0,A1=0,ties=(A1=0);
        name=UserFunction,Formula=Intensity*exp(-(x/Tau)^Beta),Intensity=1.0,Tau=0.1,Beta=1;ties=(f1.Intensity=1-f0.A0)
    );
    """.replace('$WORKSPACE$',inputWS)
    func= 'composite=MultiBG;'
    ties='ties=('
    for i in range(0,nHist):
        func+=f1.replace('$INDEX$',str(i))
        if i > 0:
            ties += 'f' + str(i) + '.f1.Beta=f0.f1.Beta'
            if i < nHist-1:
                ties += ','
    ties+=')'
    func += ties
    logger.notice(func)
    Fit(InputWorkspace=inputWS,Function=func,Output=outNm)
    wsname = furyfitMultParsToWS(outNm, inputWS)
    if Save:
        opath = os.path.join(workdir, wsname+'.nxs')					# path name for nxs file
        SaveNexusProcessed(InputWorkspace=wsname, Filename=opath)
        if Verbose:
            logger.notice('Output file : '+opath)  
    if ( Plot != 'None' ):
        furyfitPlotMult(wsname, Plot)
    EndTime('FuryFit')

