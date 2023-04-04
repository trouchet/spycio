from numpy import pi

from spycio.utils import spherToCart

# Assertion tolerance
TOL=0.01
EPS=0.001

non_spherical_candidates=[
    ([]), ([42]), 
    ([-pi - EPS, 0]), 
    ([pi + EPS, 0]), 
    ([0, -EPS]), 
    ([0, 2 * pi + EPS])
]

spher_cartesian_candidates=[
    spherToCart([0, 0], 1),
    spherToCart([pi / 2, pi / 2], 1),
    spherToCart([pi / 2, 0], 1)
] 

geographical_candidate_tuples=[
    ( 90,    180, [   pi, 2*pi]) ,  
    ( 90,     0 , [   pi, pi  ]) ,  
    ( 90,   -180, [   pi, 0   ]),  
    (  0,    180, [ pi/2, 2*pi]),  
    (  0,      0, [ pi/2, pi  ]),  
    (  0,   -180, [ pi/2, 0   ]),  
    (-90,    180, [    0, 2*pi]),  
    (-90,     0 , [    0, pi  ]),  
    (-90,   -180, [    0, 0   ])  
]

spher_cartesian_norms=[ 1, 1, 1 ]

spher_cartesian_tuples=list(\
    zip(spher_cartesian_candidates, spher_cartesian_norms)\
)