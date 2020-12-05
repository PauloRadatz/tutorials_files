import py_dss_interface
import matplotlib.pyplot as plt
import numpy as np

dss_file = r"C:\py-dss-interface-MiniCurso\8500-Node\Master-unbal.dss"

dss = py_dss_interface.DSSDLL()

dss.text("compile [{}]".format(dss_file))

dss.text("New Energymeter.m1 Line.ln5815900-1 1")
dss.text("New Monitor.m1 Line.ln5815900-1 terminal=1 mode=1 ppolar=False")
dss.text("Set Maxiterations=20")
dss.text("set maxcontrolit=100")

# Q2 - 1
dss.text("Batchedit Load..* daily=default")

dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")
dss.text("solve")

# Q2 - 2
dss.loads_write_name("328365B0a")
loadshape = dss.loads_read_daily()

# Q2 - 3
dss.monitors_write_name("m1")
pa = dss.monitors_channel(1)
qa = dss.monitors_channel(2)
pb = dss.monitors_channel(3)
qb = dss.monitors_channel(4)
pc = dss.monitors_channel(5)
qc = dss.monitors_channel(6)

pt = np.array(pa) + np.array(pb) + np.array(pc)
qt = np.array(qa) + np.array(qb) + np.array(qc)

plt.plot(list(range(1, len(pt) + 1)), pt, "g", label='P')
plt.plot(list(range(1, len(qt) + 1)), qt, "b", label='Q')
plt.title("Daily Active and Reactive Power at Feeder Head")
plt.legend()
plt.ylabel("kW, kvar")
plt.xlabel("Hour")
plt.xlim(1, 24)
plt.grid(True)
plt.show()
plt.savefig(r"C:\py-dss-interface-MiniCurso\8500-Node\demand-noPV.jpg")

# Q2 - 4
pt_max = pt.max()
peak_hour = pt.argmax() + 1
dss.meters_first()

feeder_kwh = dss.meters_registervalues()[0]
loads_kwh = dss.meters_registervalues()[4]
losses_kwh = dss.meters_registervalues()[12]

print("Feeder kWh={}".format(feeder_kwh))
print("Loads kWh={}".format(loads_kwh))
print("Losses kWh={}".format(losses_kwh))


# dss.loads_first()
#
# list_carga = []
# for _ in range(dss.loads_count()):
#     list_carga.append(dss.loads_read_name())
#
#     dss.loads_next()
#
# print("here")