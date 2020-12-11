import py_dss_interface
import matplotlib.pyplot as plt
import numpy as np
import random
import add_pvs


def set_pvs(dss, pv_buses_list, bus_kvbase_dict, pv_kva, pv_kw):
    for pv_bus in pv_buses_list:
        add_pvs.define_3ph_pvsystem_with_transformer(dss, pv_bus, bus_kvbase_dict[pv_bus], pv_kva, pv_kw)
        add_pvs.add_bus_marker(dss, pv_bus, "red")

def set_generation(dss, pv_buses_list, bus_kvbase_dict, pv_kva, pv_kw):
    for pv_bus in pv_buses_list:
        add_pvs.define_3ph_generator_with_transformer(dss, pv_bus, bus_kvbase_dict[pv_bus], pv_kva, pv_kw)
        add_pvs.add_bus_marker(dss, pv_bus, "red")

model_dss = py_dss_interface.DSSDLL(r"C:\py-dss-interface-Live\Model_DSS", "OpenDSSDirect_model.dll")
real_dss = py_dss_interface.DSSDLL(r"C:\py-dss-interface-Live\Real_DSS", "OpenDSSDirect_real.dll")

model_dss_file = r"C:\py-dss-interface-Live\8500-Node_model\Master.dss"
real_dss_file = r"C:\py-dss-interface-Live\8500-Node_real\Master.dss"

real_dss.text("compile [{}]".format(real_dss_file))
real_dss.text("Set Maxiterations=100")
real_dss.text("set maxcontrolit=100")
real_dss.text("set casename=real")
real_dss.text("Batchedit Load..* daily=default")
real_dss.text("set mode=daily")
real_dss.text("set stepsize=1h")
real_dss.text("Set controlmode=Off")

bus_list = real_dss.circuit_allbusnames()
bus_3ph_list = list()
bus_kvbase_dict = dict()
for index, bus in enumerate(bus_list):
    real_dss.circuit_setactivebus(bus)
    num_phases = len(real_dss.bus_nodes())
    kv_base = real_dss.bus_kVbase()

    if num_phases == 3 and kv_base > 1.0:
        bus_3ph_list.append(bus)
        bus_kvbase_dict[bus] = kv_base

random.seed(114)
pv_buses_list = random.sample(bus_3ph_list, 5)

pv_kva = 1100
pv_kw = 1000
set_pvs(real_dss, pv_buses_list, bus_kvbase_dict, pv_kva, pv_kw)

# real_dss.text("Solve")
real_dss.text("Plot Circuit Power Max=2000 dots=n labels=n  C1=Blue  1ph=3")

q_min_losses = 0
for hour in range(0, 24):
    print(f"Hour: {hour}")

    real_dss.pvsystems_first()
    for _ in range(real_dss.pvsystems_count()):
        real_dss.text(f"edit pvsystem.{real_dss.pvsystems_read_name()} kvar={q_min_losses}")
        real_dss.pvsystems_next()
    real_dss.text("set hour={}".format(hour))
    real_dss.text("solve")

    # Measure active power of PVSystems
    gen_kw_dict = dict()
    gen_kvar_dict = dict()
    real_dss.pvsystems_first()
    for _ in range(real_dss.pvsystems_count()):
        gen_kw_dict[real_dss.pvsystems_read_name()] = -1 * sum(real_dss.cktelement_powers()[0::2])
        gen_kvar_dict[real_dss.pvsystems_read_name()] = -1 * sum(real_dss.cktelement_powers()[1::2])
        real_dss.pvsystems_next()

    # Measure Active power of Loads
    load_kw_dict = dict()
    real_dss.loads_first()
    for _ in range(real_dss.loads_count()):
        load_kw_dict[real_dss.loads_read_name()] = sum(real_dss.cktelement_powers()[0::2])
        real_dss.loads_next()

    # Set feeder model with PVSystem and Load active power for timestep t
    model_dss.text("compile [{}]".format(model_dss_file))
    model_dss.text("Set Maxiterations=1000")
    model_dss.text("set maxcontrolit=1000")
    model_dss.text("set casename=Model")
    model_dss.text("Set controlmode=Off")

    set_generation(model_dss, pv_buses_list, bus_kvbase_dict, pv_kva, pv_kw)

    # Set active power of Generators
    model_dss.generators_first()
    for _ in range(model_dss.generators_count()):
        model_dss.generators_write_kw(gen_kw_dict[model_dss.generators_read_name()])
        model_dss.generators_next()

    # Set active power of loads
    model_dss.loads_first()
    for _ in range(model_dss.loads_count()):
        model_dss.loads_write_kw(load_kw_dict[model_dss.loads_read_name()])
        model_dss.loads_next()

    model_dss.text("solve")

    # Algorithm to set the reactive power that minimize losses
    q_option_list = [-400, -300, 200, 300, 400]

    losses_dict = dict()
    for q in q_option_list:
        model_dss.generators_first()
        for _ in range(model_dss.generators_count()):
            model_dss.generators_write_kvar(q)
            model_dss.generators_next()
        model_dss.text("solve")
        losses_dict[q] = model_dss.circuit_losses()[0]

    q_min_losses = min(losses_dict.keys(), key=(lambda k: losses_dict[k]))

print("here")