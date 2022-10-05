RefinePowderDiffProfileSeq(
        InputWorkspace  = "PG3_15035",
        WorkspaceIndex  = 0,
        SeqControlInfoWorkspace = "RecordTest001Table",
        StartX  = 10000.,
        EndX    = 79000.,
        FunctionOption      = "Refine",
        RefinementOption    = "Random Walk",
        ParametersToRefine  = "Alph0, Beta0",
        NumRefineCycles     = 1000,
        #FromStep           = 1,
        ProjectID           = "Test001")
