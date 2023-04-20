from numpy import pi, linspace, sqrt, Inf
from itertools import product

from spycio.utils import spherToCart, spherToGeo

def toParameter(names, variables):
    return {
        "names": names,
        "variables": variables
    }

# Assertion tolerance
TOL=0.01
EPS=0.001

non_spherical_candidates=toParameter(
    "candidate",
    [
        ([]), ([42]), 
        ([-pi - EPS, 0]), 
        ([pi + EPS, 0]), 
        ([0, -EPS]), 
        ([0, 2 * pi + EPS])
    ]
)

non_spherical_candidate_tuples=toParameter(
    "candidate1,candidate2",
    [
        ([], []), ([42], []), 
        ([-pi - EPS, 0], []), 
        ([pi + EPS, 0], []), 
        ([0, -EPS], []), 
        ([0, 2 * pi + EPS], [])
    ]
)

non_geographical_candidates=toParameter(
    "candidate",
    [
        ([]), ([42]), 
        ([-pi/2 - EPS, 0]), 
        ([pi/2 + EPS, 0]), 
        ([0, -pi-EPS]), 
        ([0, pi + EPS])
    ]
)

n_phi=5
n_lambda=5

lambda_bottom=0
lambda_upper=3

phi_bottom=0
phi_upper=6

spherical_coordinates=toParameter(\
    "coordinates", 
    list(
        product(\
            linspace(lambda_bottom, lambda_upper, n_phi), \
            linspace(phi_bottom, phi_upper, n_lambda)
        )
    )
)



lat_bottom=-90
lat_upper=90

lng_bottom=-180
lng_upper=180

geographical_coordinates=toParameter(\
    "coordinates", 
    list(
        product(\
            linspace(lat_bottom, lat_upper, n_phi), \
            linspace(lng_bottom, lng_upper, n_lambda)
        )
    )
)

distance_setups=toParameter(\
    "average_speed,coordinate_1,coordinate_2,method,method_config,expected_value", \
    [
        (1, [1, 1], [2, 2], "pnorm", { "exponent": 2 }, sqrt(2)),
        (1, [1, -1], [2, 2], "pnorm", { "exponent": Inf }, 3),
        (1, [0, 0], [pi / 2, 0], "sphere", { "radius": 1 }, (2 * pi) / 4),
        (1, spherToGeo([0, 0]), spherToGeo([pi / 2, 0]), "geographical", { "radius": 1 }, (2 * pi) / 4),
        (2, [1, 1], [2, 2], "pnorm", { "exponent": 2 }, sqrt(2) / 2),
        (2, [1, -1], [2, 2], "pnorm", { "exponent": Inf }, 1.5),
        (2, [0, 0], [pi / 2, 0], "sphere", { "radius": 1 }, (2 * pi) / 8),
        (2, spherToGeo([0, 0]), spherToGeo([pi / 2, 0]), "geographical", { "radius": 1 }, (2 * pi) / 8),
    ]\
)

A=[1, 1]
B=[2, 2]

distance_setups_without_config=toParameter(\
    "average_speed,coordinate_1,coordinate_2,method,expected_value",
    [
        (1, A, B, "manhattan", 2),
        (1, A, B, "cityblock", 2),
        (1, A, B, "euclidean", sqrt(2)),
        (1, A, B, "max", 1),
        (1, A, B, "chebyshev", 1),
        (1, A, B, "cosine", 2.22e-16),
        (1, A, B, "braycurtis", 1/3),
        (1, A, B, "canberra", 2/3)
    ]
)

geographical_candidate_tuples=toParameter(\
    "latitude,longitude,spher_coordinates", \
    [
        ( 90,    180, [   pi, 2*pi]) ,  
        ( 90,     0 , [   pi, pi  ]) ,  
        ( 90,   -180, [   pi, 0   ]),  
        (  0,    180, [ pi/2, 2*pi]),  
        (  0,      0, [ pi/2, pi  ]),  
        (  0,   -180, [ pi/2, 0   ]),  
        (-90,    180, [    0, 2*pi]),  
        (-90,     0 , [    0, pi  ]),  
        (-90,   -180, [    0, 0   ])  
    ]\
)

spher_cartesian_candidates=[
    spherToCart([0, 0], 1),
    spherToCart([pi / 2, pi / 2], 1),
    spherToCart([pi / 2, 0], 1)
] 
spher_cartesian_norms=[ 1, 1, 1 ]

spher_cartesian_tuples=toParameter(\
    "candidate, norm_value", list(zip(spher_cartesian_candidates, spher_cartesian_norms))
)

pnorm_fixtures=toParameter("exponent,expected_value", [ (1, 2), (2, sqrt(2)), (Inf, 1), ])