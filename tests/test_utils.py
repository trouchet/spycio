from pytest import mark, raises
from math import isclose
from numpy import pi

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

def test_hav():
    assert isclose(hav(pi), 1, abs_tol=TOL)
    assert isclose(hav(2 * pi), 0, abs_tol=TOL)

@mark.parametrize(geographical_candidate_tuples["names"], geographical_candidate_tuples["variables"])
def test_geoToSpher(latitude, longitude, spher_coordinates):
    geocoordinates=geoToSpher(latitude, longitude)
    
    assert geocoordinates == spher_coordinates
    assert isSpherical(geocoordinates) == True

@mark.parametrize(spher_cartesian_tuples["names"], spher_cartesian_tuples["variables"])
def test_spherToCart_candidates(candidate, norm_value):
    assert isclose(pNorm(candidate, 2), norm_value, abs_tol=TOL)

@mark.parametrize(non_spherical_candidates["names"], non_spherical_candidates["variables"])
def test_isSpherical(candidate):
    assert isSpherical(candidate) == False 

@mark.parametrize(non_spherical_candidates["names"], non_spherical_candidates["variables"])
def test_spherToCart(candidate):
    R=1
    
    with raises(TypeError):
        assert spherToCart(candidate, R)

@mark.parametrize(spherical_coordinates["names"], spherical_coordinates["variables"])
def test_isSpherical_batch(theta, phi):
    assert isSpherical([theta, phi]) == True