NEURON {
       
		
		SUFFIX sump
			POINTER Trl
        USEION x READ xi, xo WRITE ix VALENCE 1
        NONSPECIFIC_CURRENT i
        RANGE ix, rate
}

UNITS {
	(mV)	= (millivolt)
	(molar) = (1/liter)
	(mM)	= (millimolar)
	(mA)	= (milliamp)
}


PARAMETER {
    imax=1    (mA/cm2)
    Kd      (mM)
}

INITIAL {
    ix = 0
    :Kd = 1.0
}
 
ASSIGNED {
    xo      (mM)
    xi      (mM)
    ix      (mA/cm2)
    i       (mA/cm2)
	Trl 	(mM)
}
 
BREAKPOINT {
    ix = imax*Trl 
    i = -ix
}