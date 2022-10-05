def do_plot_1d(data, vertical, title):
	if vertical:
		g = plotBin(data, 0)
	else:
		g = plotSpectrum(data, 0)
	g.activeLayer().setTitle(title)
# end def

raw = Load(Filename="MAR11001.raw")

do_plot_1d(raw, vertical=False, title="spectrum axis on Y, numeric on X")
do_plot_1d(raw, vertical=True, title="numeric axis on Y, spectrum on X")

theta = ConvertSpectrumAxis(raw,Target="Theta")
do_plot_1d(theta, vertical=False, title="numeric axis on Y, numeric on X.")
do_plot_1d(theta, vertical=True, title="numeric axis on Y, numeric on X. ")

# 
distr = CloneWorkspace(raw)
ConvertToDistribution(distr)
do_plot_1d(distr, vertical=False, title="spectrum axis on Y. numeric on X. WS is distribution")
do_plot_1d(distr, vertical=True, title="numeric axis on Y. spectrum X. WS is distribution")

#
theta_distr = CloneWorkspace(theta)
ConvertToDistribution(theta_distr)
do_plot_1d(theta_distr, vertical=False, title="numeric axis on Y. numeric on X. WS is distribution")
do_plot_1d(theta_distr, vertical=True, title="numeric axis on Y. numeric X. WS is distribution")

##################################################################
# 2D
def do_plot_2d(data, title):
	mm = importMatrixWorkspace(str(data))
	g = mm.plotGraph2D()
	g.activeLayer().setTitle(title)
# end def

#
do_plot_2d(raw, "spectrum axis on Y, numeric on X")
#
do_plot_2d(theta, "numeric axis on Y, numeric on X")
#
do_plot_2d(distr, "spectrum axis on Y, numeric on X. WS is distribution")

#
do_plot_2d(theta_distr, "numeric axis on Y, numeric on X. WS is distribution")

