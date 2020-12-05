def define_3ph_pvsystem_with_transformer(dss, bus, kv, kva, pmpp):

    dss.text("New line.PV_{} phases=3 bus1={} bus2=PV_sec_{} switch=yes".format(bus, bus, bus))
    dss.text("New transformer.PV_{} phases=3 windings=2 buses=(PV_sec_{}, PV_ter_{}) conns=(wye, wye) kVs=({},0.48) "
             "xhl=5.67 %R=0.4726 kVAs=({}, {})".format(bus, bus, bus, kv, kva, kva))

    dss.text("makebuslist")
    dss.text("setkVBase bus=PV_sec_{} kVLL={}".format(bus, kv))
    dss.text("setkVBase bus=PV_ter_{} kVLL=0.48".format(bus))

    dss.text("New XYCurve.MyPvsT npts=4  xarray=[0  25  75  100]  yarray=[1.2 1.0 0.8  0.6]")
    dss.text("New XYCurve.MyEff npts=4  xarray=[.1  .2  .4  1.0]  yarray=[.86  .9  .93  .97]")
    dss.text("New Loadshape.MyIrrad npts=24 interval=1 mult=[0 0 0 0 0 0 .1 .2 .3  .5  .8  .9  1.0  1.0  .99  .9  .7  .4  .1 0  0  0  0  0]")
    dss.text("New Tshape.MyTemp npts=24 interval=1 temp=[25, 25, 25, 25, 25, 25, 25, 25, 35, 40, 45, 50  60 60  55 40  35  30  25 25 25 25 25 25]")


    dss.text("New PVSystem.PV_{} phases=3 conn=wye  bus1=PV_ter_{} kV=0.48 kVA={} Pmpp={} pf=1 %cutin=0.00005 %cutout=0.00005 VarFollowInverter=yes"
             " effcurve=Myeff  P-TCurve=MyPvsT Daily=MyIrrad  TDaily=MyTemp".format(bus, bus, kva, pmpp))
    dss.text("New monitor.PV_{}_V element=transformer.PV_{} terminal=2 mode=0".format(bus, bus))
    dss.text("New monitor.PV_{}_P element=transformer.PV_{} terminal=2 mode=1 ppolar=no".format(bus, bus))
    dss.text("New monitor.PV_{}_M element=PVSystem.PV_{} terminal=1 mode=3".format(bus, bus))

def add_bus_marker(dss, bus, color, size_marker=8, code=15):
    dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus, color, size_marker, code))