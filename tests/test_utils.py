from spycio.utils import radianToDegree, degreeToRadian, \
    geoToSpher, hav, isSpherical, throw, hasKey
from spycio.spycio import pNorm
from .fixtures import TOL

from pytest import mark
from math import isclose
from numpy import pi, arange

from .fixtures import non_spherical_candidates, spher_cartesian_candidates

def test_radian_to_degree():
    assert radianToDegree(pi) == 180

def test_degree_to_radian():
    assert degreeToRadian(180) == pi

def test_geoToSpher():
    assert geoToSpher(0, 0) == [pi / 2, 0]

def test_geoToSpher():
    assert geoToSpher(0, 0) == [pi / 2, 0]

@mark.parametrize("candidate, norm_value", spher_cartesian_candidates)
def test_spherToCart(candidate, norm_value):
    assert isclose(pNorm(candidate, 2), norm_value, abs_tol=TOL)

def test_hav():
    assert isclose(hav(pi), 1, abs_tol=TOL)
    assert isclose(hav(2 * pi), 0, abs_tol=TOL)

@mark.parametrize("candidate", non_spherical_candidates)
def test_isSpherical(candidate):
    assert isSpherical(candidate) == False 

def test_isSpherical_batch():
    thetas = arange(-3, 3, (2 * pi) / 8)
    phis = arange(0, 6, (2 * pi) / 8)

    for theta in thetas:
        for phi in phis:
            assert isSpherical([theta, phi]) == True