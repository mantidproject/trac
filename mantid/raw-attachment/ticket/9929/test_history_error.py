ws = Load('INTER00007709.nxs')
ws, wave, theta = ReflectometryReductionOneAuto(ws)
history = ws.getHistory()
alg_hist = history.getAlgorithmHistory(1)
alg_hist = alg_hist.getChildAlgorithmHistory(0)
alg = alg_hist.getChildAlgorithm(1)