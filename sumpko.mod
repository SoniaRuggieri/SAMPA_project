NEURON {
       
		
		SUFFIX sumpko
			POINTER Trl
        USEION xko READ xkoi, xkoo WRITE ixko VALENCE 1
        NONSPECIFIC_CURRENT i
        RANGE ixko, rate
}

UNITS {
	(mV)	= (millivolt)
	(molar) = (1/liter)
	(mM)	= (millimolar)
	(mA)	= (milliamp)
}


PARAMETER {
    imaxko=1    (mA/cm2)
    Kd      (mM)
}

INITIAL {
    ixko = 0
    Kd = 1.0
}
 
ASSIGNED {
    xkoo      (mM)
    xkoi      (mM)
    ixko      (mA/cm2)
    i       (mA/cm2)
	Trl 	(mM)
}
 
BREAKPOINT {
    ixko = imaxko*Trl/Kd
    i = -ixko
}

:ix = imax * (xi/(Kd + xi) - xo/(Kd + xo))