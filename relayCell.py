from neuron import h
h.load_file('geom_pyr.hoc')

class relayCell():
    def __init__(self):
        self.cell = h.relay()
        