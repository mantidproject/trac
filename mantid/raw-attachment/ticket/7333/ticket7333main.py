""" Main test script for ticket 7333 """
Load(Filename=r'PG3_4844_event.nxs',
        OutputWorkspace='PG3_4844')
inws = mtd["PG3_4844"]

FilterBadPulses(InputWorkspace='PG3_4844',
        OutputWorkspace='PG3_4844')

AlignAndFocusPowder(
        InputWorkspace='PG3_4844',
        OutputWorkspace='PG3_4844_High',
        LowResTOFWorkspace="PG3_4844_Low",
        CalFileName=r'PG3_FERNS_d4832_2011_08_24.cal',
        Params='-0.0004',DMin='0.1',
        DMax='2.2',
        TMax='16666.669999999998',
        RemovePromptPulseWidth='50',
        LowResRef='15000')
