NEURON {
       
		
		SUFFIX sumpwt
			POINTER Trl
        USEION xwt READ xwti, xwto WRITE ixwt VALENCE 1
        NONSPECIFIC_CURRENT i
        RANGE ixwt, rate, imaxwt
}

UNITS {
	(mV)	= (millivolt)
	(molar) = (1/liter)
	(mM)	= (millimolar)
	(mA)	= (milliamp)
}


PARAMETER {
    imaxwt=1    (mA/cm2)
    Kd      (mM)
}

INITIAL {
    ixwt = 0
    Kd = 1.0
}
 
ASSIGNED {
    xwto      (mM)
    xwti      (mM)
    ixwt      (mA/cm2)
    i       (mA/cm2)
	Trl 	(mM)
}
 
BREAKPOINT {
    ixwt = imaxwt*Trl/Kd:*xwti/(Kd + xwti): ( - xwto/(Kd + xwto)) 
    i = -ixwt
}