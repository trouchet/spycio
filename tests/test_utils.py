from spycio.utils import radianToDegree, degreeToRadian, \
    geoToSpher, hav, spherToCart, isSpherical, throw, hasKey
from spycio.spycio import pNorm

from math import isclose
from numpy import pi, arange

# Assertion tolerance
TOL=0.01
EPS=0.001

def test_radian_to_degree():
    assert radianToDegree(pi) == 180

def test_degree_to_radian():
    assert degreeToRadian(180) == pi

def test_geoToSpher():
    assert geoToSpher(0, 0) == [pi / 2, 0]

def test_geoToSpher():
    assert geoToSpher(0, 0) == [pi / 2, 0]

'''
def test_spherToCart():
    assert isclose(pNorm(spherToCart([0, 0], 1), 2), 1)
    assert isclose(pNorm(spherToCart([pi / 2, 0], 1), 2), 1)
    assert isclose(pNorm(spherToCart([pi / 2, pi / 2], 1), 2), 1)
'''

'''    
def test_hav():
    assert isclose(hav(pi), 1)
    assert isclose(hav(2 * pi), 0)
'''
    
def test_isSpherical():
    assert isSpherical([]) == False 
    assert isSpherical([42]) == False
    assert isSpherical([-pi - EPS, 0]) == False
    assert isSpherical([pi + EPS, 0]) == False
    assert isSpherical([0, -EPS]) == False
    assert isSpherical([0, 2 * pi + EPS]) == False

def test_isSpherical_batch():
    thetas = arange(-3, 3, (2 * pi) / 8)
    phis = arange(0, 6, (2 * pi) / 8)

    for theta in thetas:
        for phi in phis:
            assert isSpherical([theta, phi]) == True