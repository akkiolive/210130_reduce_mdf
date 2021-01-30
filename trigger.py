from asammdf import MDF, Signal

mdf = MDF(version="3.00")

s1 = Signal([100, 123, 123],[10, 11, 12],name="signal_1")
mdf.append(s1)
mdf.add_trigger(0, timestamp=10, comment="hogae")

mdf.save("trig")
