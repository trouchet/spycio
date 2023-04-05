from pytest import mark, raises
from math import isclose
from numpy import pi, arange

from spycio.utils import radianToDegree, degreeToRadian, \
    geoToSpher, hav, isSpherical, spherToCart
from spycio.spycio import pNorm

from .fixtures import TOL

from .fixtures import non_spherical_candidates, \
    spher_cartesian_tuples, geographical_candidate_tuples, \
    spherical_coordinates

def test_radian_to_degree():
    assert radianToDegree(pi) == 180

def test_degree_to_radian():
    assert degreeToRadian(180) == pi

@mark.parametrize("latitude,longitude,spher_coordinates", geographical_candidate_tuples)
def test_geoToSpher(latitude, longitude, spher_coordinates):
    assert geoToSpher(latitude, longitude) == spher_coordinates

@mark.parametrize("latitude,longitude,spher_coordinates", geographical_candidate_tuples)
def test_geoToSpher(latitude, longitude, spher_coordinates):
    assert isSpherical(geoToSpher(latitude, longitude)) == True

@mark.parametrize("candidate, norm_value", spher_cartesian_tuples)
def test_spherToCart_candidates(candidate, norm_value):
    assert isclose(pNorm(candidate, 2), norm_value, abs_tol=TOL)

def test_hav():
    assert isclose(hav(pi), 1, abs_tol=TOL)
    assert isclose(hav(2 * pi), 0, abs_tol=TOL)

@mark.parametrize("candidate", non_spherical_candidates)
def test_isSpherical(candidate):
    assert isSpherical(candidate) == False 

@mark.parametrize("candidate", non_spherical_candidates)
def test_spherToCart(candidate):
    R=1
    
    with raises(TypeError):
        assert spherToCart(candidate, R)


@mark.parametrize("theta, phi", spherical_coordinates)
def test_isSpherical_batch(theta, phi):
    assert isSpherical([theta, phi]) == True