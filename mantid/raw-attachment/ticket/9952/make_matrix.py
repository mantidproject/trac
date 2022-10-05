m = newMatrix("test_matrix", 1000, 1000)
m.setFormula("x*y")
m.calculate()
g = plot(m)
