from __future__ import annotations

from pytest import mark, raises, warns
from math import isclose

from numpy import sqrt, Inf, pi

from spycio.spycio import pNorm, distance, pNormDistance, \
    greatCircleDistance, nSphereDistance, travelTime

from .fixtures import TOL, distance_setups, distance_setups_without_config, \
    pnorm_fixtures, non_spherical_candidate_tuples

def test_pNorm():
    coords = [1, 1, 1, 1, 1]

    result = pNorm(coords, 2)
    expected = sqrt(5)

    assert isclose(result, expected, rel_tol=TOL)

def test_pNormDistance_error():
    coord_1 = [1, -1]
    coord_2 = [2, 2]

    emsg="The exponent n must be a number greater or equal to 1!"

    with raises(Exception):
        assert pNormDistance(coord_1, coord_2, -1), emsg


def test_greatCircleDistance():
    coord_1 = [0, 0]
    coord_2 = [0, pi / 2]
    coord_3 = [pi / 2, 0]
    radius = 1

    result = greatCircleDistance(coord_1, coord_2, radius)
    expected = pi / 2

    assert isclose(result, expected, rel_tol=TOL)

    result = greatCircleDistance(coord_1, coord_3, radius)
    expected = pi / 2

    assert isclose(result, expected, rel_tol=TOL)

    result = greatCircleDistance(coord_2, coord_3, radius)
    expected = pi / 2

    assert isclose(result, expected, rel_tol=TOL)


def test_nSphereDistance():
    coord_1 = [0, 0]
    coord_2 = [pi / 2, 0]
    coord_3 = [pi, 0]
    radius = 1
    
    assert nSphereDistance(coord_1, coord_2, radius) == \
    greatCircleDistance(coord_1, coord_2, radius)

    assert nSphereDistance(coord_1, coord_3, radius) == \
    greatCircleDistance(coord_1, coord_3, radius)

    assert nSphereDistance(coord_2, coord_3, radius) == \
    greatCircleDistance(coord_2, coord_3, radius)

    expected = (2 * pi * radius) / 4
    result = nSphereDistance(coord_1, coord_2, radius)

    assert isclose(result, expected, rel_tol=TOL)

    result = nSphereDistance(coord_1, coord_3, radius)
    expected = (2 * pi * radius) / 2

    assert isclose(result, expected, rel_tol=TOL)

    result = nSphereDistance(coord_2, coord_3, radius)
    expected = (2 * pi * radius) / 4

    assert isclose(result, expected, rel_tol=TOL)

@mark.parametrize(distance_setups["names"], distance_setups["variables"])
def test_travelTime(\
    average_speed, coordinate_1, coordinate_2, method, method_config, expected_value \
):
    result = travelTime( \
        average_speed, \
        coordinate_1, \
        coordinate_2, \
        method, \
        method_config \
    )

    assert isclose(result, expected_value, rel_tol=TOL)

@mark.parametrize(\
    distance_setups_without_config["names"] , \
    distance_setups_without_config["variables"] \
)
def test_travelTime_without_methodConfig(\
    average_speed, coordinate_1, coordinate_2, method, expected_value \
):
    result = travelTime(average_speed, coordinate_1, coordinate_2, method)

    assert isclose(result, expected_value, rel_tol=TOL)

def test_distance_pnorm_without_config():
    coordinate_1=[0,0]
    coordinate_2=[1,1]
    method='pnorm'
    
    with warns(UserWarning):
        assert distance(coordinate_1, coordinate_2, method) == sqrt(2) 

def test_distance_error_missingMethod():
    coord_1 = [1, -1]
    coord_2 = [2, 2]
    wrong_method=""
    wrong_config={}
    
    emsg="There are only the following methods available: ['pnorm', 'sphere', 'euclidean', 'manhattan', 'max']"

    with raises(TypeError):
        assert distance(coord_1, coord_2, wrong_method, wrong_config), emsg
    
    emsg="There must exist property 'radius' on config argument 'methodConfig'!"
    with raises(TypeError):
        assert distance(coord_1, coord_2, "sphere", {}), emsg

@mark.parametrize(pnorm_fixtures["names"], pnorm_fixtures["variables"])
def test_distance_pnorm(exponent, expected_value):
    """
    Generates the distance between points
    """
    method="pnorm"

    coord_1 = [1, 1]
    coord_2 = [2, 2]
    config={'exponent': exponent}

    result=distance(coord_1, coord_2, method, config)
    
    assert isclose(result, expected_value, rel_tol=TOL)

def test_distance_pnorm_Inf():
    coord_1 = [1, -1]
    coord_2 = [2, 2]

    method="pnorm"
    config={ "exponent": Inf }

    result=distance(coord_1, coord_2, method, config)
    expected=3
    
    assert isclose(result, expected, rel_tol=TOL)

def test_distance_manhattan():
    """
    Generates the manhattan distance between points
    """
    
    coord_1 = [0, 0]
    coord_2 = [1, 1]
    method="manhattan"
    
    result=distance(coord_1, coord_2, method)
    expected=2

    assert isclose(result, expected, rel_tol=TOL)

    method="cityblock"
    
    result=distance(coord_1, coord_2, method)
    expected=2

    assert isclose(result, expected, rel_tol=TOL)

def test_distance_max():
    """
    Generates the max distance between points
    """
    
    coord_1 = [0, 0]
    coord_2 = [1, 1]
    method="max"
    
    result=distance(coord_1, coord_2, method)
    expected=1

    assert isclose(result, expected, rel_tol=TOL)

    method="chebyshev"
    
    result=distance(coord_1, coord_2, method)
    expected=1

    assert isclose(result, expected, rel_tol=TOL)

def test_distance_euclidean():
    """
    Generates the euclidean distance between points
    """
    
    coord_1 = [0, 0]
    coord_2 = [1, 1]
    method="euclidean"
    
    result=distance(coord_1, coord_2, method)
    expected=sqrt(2)

    assert isclose(result, expected, rel_tol=TOL)

    method="sqeuclidean"
    result=distance(coord_1, coord_2, method)
    expected=2

    assert isclose(result, expected, rel_tol=TOL)

@mark.parametrize(non_spherical_candidate_tuples["names"], non_spherical_candidate_tuples["variables"])
def test_distance_sphere_error_nonSpherical(candidate1,candidate2):
    method="sphere"
    config={ "radius": 1 }

    with raises(TypeError):
        assert distance(candidate1, candidate2, method, config)

def test_distance_sphere():
    """
    Generates the sphere distance between points
    """
    
    coord_1 = [0, 0]
    coord_2 = [pi / 2, 0]
    method="sphere"
    config={ "radius": 1 }
    
    result=distance(coord_1, coord_2, method, config)
    expected=(2 * pi) / 4

    assert isclose(result, expected, rel_tol=TOL)