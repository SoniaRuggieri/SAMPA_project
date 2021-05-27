from neuron import h
h.load_file('geom_pyr.hoc')

class relay():
    def __init__(self):
        self.cell = h.init()
