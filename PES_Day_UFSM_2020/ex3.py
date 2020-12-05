import py_dss_interface
import matplotlib.pyplot as plt
import numpy as np
import random
import functions


def get_monitor_values(dss, name):
    dss.monitors_write_name(name)
    va = dss.monitors_channel(1)
    vaa = dss.monitors_channel(2)

    return va, vaa

def run(pv_kva, pv_kw):
    random.seed(114)
    dss_file = r"C:\py-dss-interface-MiniCurso\8500-Node\Master-unbal.dss"
    dss = py_dss_interface.DSSDLL()
    dss.text("compile [{}]".format(dss_file))
    dss.text("New Energymeter.m1 Line.ln5815900-1 1")
    dss.text("New Monitor.m1 Line.ln5815900-1 terminal=1 mode=1 ppolar=False")
    dss.text("Set Maxiterations=20")
    dss.text("set maxcontrolit=100")
    dss.text("Batchedit Load..* daily=default")
    # Q3 PVs
    bus_list = dss.circuit_allbusnames()
    bus_3ph_list = list()
    bus_kvbase_dict = dict()
    for index, bus in enumerate(bus_list):
        dss.circuit_setactivebus(bus)
        num_phases = len(dss.bus_nodes())
        kv_base = dss.bus_kVbase()

        if num_phases == 3 and kv_base > 1.0:
            bus_3ph_list.append(bus)
            bus_kvbase_dict[bus] = kv_base
    pv_buses_list = random.sample(bus_3ph_list, 5)
    for pv_bus in pv_buses_list:
        functions.define_3ph_pvsystem_with_transformer(dss, pv_bus, bus_kvbase_dict[pv_bus], pv_kva, pv_kw)
        functions.add_bus_marker(dss, pv_bus, "red")
    dss.text("set mode=daily")
    dss.text("set number=24")
    dss.text("set stepsize=1h")
    dss.text("solve")
    dss.text("Plot Circuit Power Max=2000 dots=n labels=n  C1=Blue  1ph=3")
    # Q3 - 2
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
    plt.title("Daily Active and Reactive Power at Feeder Head with PVs")
    plt.legend()
    plt.ylabel("kW, kvar")
    plt.xlabel("Hour")
    plt.xlim(1, 24)
    plt.grid(True)
    # plt.show()
    plt.savefig(r"C:\py-dss-interface-MiniCurso\8500-Node\demand-{}.jpg".format(pv_kw))
    # Q3 - 1
    pt_max = pt.max()
    peak_hour = pt.argmax() + 1

    dss.meters_first()
    feeder_kwh = dss.meters_registervalues()[0]
    loads_kwh = dss.meters_registervalues()[4]
    losses_kwh = dss.meters_registervalues()[12]
    pv_kwh = loads_kwh + losses_kwh - feeder_kwh

    va, vaa = get_monitor_values(dss, dss.monitors_allnames()[1])

    print("here")

    return feeder_kwh, loads_kwh, losses_kwh, pv_kwh


pv_kw_array = 1000.0 * np.array([0.5, 1.0, 1.5])
pv_kva_array = 1.1 * pv_kw_array

for i in range(len(pv_kw_array)):
    feeder_kwh, losses_kwh, loads_kwh, pv_kwh = run(pv_kva_array[i], pv_kw_array[i])

    print("Scenario {}.".format(i + 1))
    print("Feeder kWh={}".format(feeder_kwh))
    print("Loads kWh={}".format(loads_kwh))
    print("Losses kWh={}".format(losses_kwh))
    print("PVs kWh={}\n\n".format(pv_kwh))

