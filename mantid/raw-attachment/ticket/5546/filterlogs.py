period = 17
ws = mtd['POLREF00006224_' + str(period)]
run = ws.getRun()
temperature_log = run.getLogData('methantemp')

period_log =run.getLogData('period ' + str(period))
filter = LogFilter(temperature_log)
filter.addFilter(period_log)
filtered_log = filter.data()

print period, temperature_log.size(), filtered_log.size()