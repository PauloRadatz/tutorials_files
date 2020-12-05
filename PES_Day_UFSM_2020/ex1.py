import py_dss_interface

dss_file = r"C:\py-dss-interface-MiniCurso\8500-Node\Master-unbal.dss"

dss = py_dss_interface.DSSDLL()

dss.text("compile [{}]".format(dss_file))

dss.text("New Energymeter.m1 Line.ln5815900-1 1")
dss.text("Set Maxiterations=20")

dss.solution_solve()

# Q1 - 1
p_mw = -1 * dss.circuit_totalpower()[0] / 10 ** 3
q_mvar = -1 * dss.circuit_totalpower()[1] / 10 ** 3

# Q1 - 2
losses_mw = dss.circuit_losses()[0] / 10 ** 6
losses_mvar = dss.circuit_losses()[1] / 10 ** 6

# Q1 - 3
lines_losses_mw = dss.circuit_linelosses()[0] / 10 ** 3
lines_losses_mvar = dss.circuit_linelosses()[1] / 10 ** 3

transformers_losses_mw = losses_mw - lines_losses_mw
transformers_losses_mvar = losses_mvar - lines_losses_mvar

# Q1 - 4
# a)
dss.lines_write_name("LN6379462-3")
bus1 = dss.lines_read_bus1()
bus2 = dss.lines_read_bus2()

# b)
dss.circuit_setactiveelement("Line.LN6379462-3")
voltages = dss.cktelement_voltagesmagang()
currents = dss.cktelement_currentsmagang()

# c)
power_in = dss.cktelement_powers()[0:6]


# Q1 - 5
dss.circuit_setactivebus(bus1)
voltages_bus1 = dss.bus_vmagangle()


# Q1 - 6

dss.loads_first()
kw_load_max = 0.0

for _ in range(dss.loads_count()):

    kw_load = dss.loads_read_kw()
    if kw_load > kw_load_max:
        load_name = dss.loads_read_name()
        kw_load_max = kw_load
        kw_load_powerflow = dss.cktelement_powers()[0]

    dss.loads_next()

# dss.circuit_setactiveelement("Load.{}".format(load_name))
# kw_load_powerflow = dss.cktelement_powers()[0]

# Q1 - 7
dss.text("Plot Profile Phases=All")

print("here")