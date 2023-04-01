"""Main module."""
import numpy as np
from numpy import max, abs, arcsin, sqrt, Inf
from functools import reduce
from warnings import warn

from .utils import hav, arguv, spherToCart, isSpherical, throw, objectHasKey

'''
  @abstract n-norm of a number
 
  @param {Array} arr
  @param {Number} n
  @return {Number}
'''
def nNorm(arr, n):
  nNormFun=lambda dist, elem: dist + abs(elem) ** n
  redSum = reduce(nNormFun, arr, 0)

  return redSum ** (1 / n)

'''
  @abstract returns the n-norm of a vector
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {Number} n
  @return {Number}
'''
def nNormDistance(coordinate_1, coordinate_2, n):
  if (n < 1):
    throw("The exponent n must be a number greater or equal to 1!")

  diffAbsFun=lambda coord_1, coord_2: abs(coord_1 - coord_2)
  coordiff = map(diffAbsFun, zip(coordinate_1, coordinate_2))

  return max(coordiff) if n == Inf else nNorm(coordiff, n)

'''
  @abstract returns the central angle between two coordinate points on a sphere
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {Number} n
  @return {Number}
'''
def sphereCentralAngle(coordinate_1, coordinate_2):
  longitude_1 = coordinate_1[0]
  longitude_2 = coordinate_2[0]
  
  latitude_1 = coordinate_1[1]
  latitude_2 = coordinate_2[1]
  
  aux_1 = 1 - hav(latitude_1 - latitude_2) - hav(latitude_1 + latitude_2)
  aux_2 = hav(longitude_2 - longitude_1)
  aux_3 = hav(latitude_2 - latitude_1)
  
  hav_theta = aux_3 + aux_2 * aux_1

  return 2 * arcsin(sqrt(hav_theta))

def centralAngle(vector_1, vector_2, R):
  return arguv(spherToCart(vector_1, R), spherToCart(vector_2, R), 2)

'''
  @abstract returns the distance of two points on a sphere
 
  @param {Array} coord_1
  @param {Array} coord_2
  @param {Number} n
  @return {Number}
'''
def greatCircleDistance(coord_1, coord_2, R): 
  return R * sphereCentralAngle(coord_1, coord_2)

'''
  @abstract returns the distance of two points on a sphere
 
  @param {Array} coord_1
  @param {Array} coord_2
  @param {Number} n
  @return {Number}
'''
def nSphereDistance(coord_1, coord_2, R):
  return R * centralAngle(coord_1, coord_2, R)

'''
  @abstract returns the distance of two points based on
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {String} method
  @param {Object} methodConfig
  @return {Number}
'''
def distance(coordinate_1, coordinate_2, method, methodConfig):
  notification_message = "There must exist property '_placeholder_' on config argument 'methodConfig'!"

  
  if(method=="nnorm"):
    exponent=-1

    if (not objectHasKey(methodConfig, "exponent")):
      emsg=notification_message.replace("_placeholder_", "radius")
      warn(emsg, UserWarning)
      
      exponent = 2
    else:
      exponent = methodConfig.exponent

    return nNormDistance(coordinate_1, coordinate_2, exponent)

  elif(method=="sphere"):
    are_spherical = not isSpherical(coordinate_1) or not isSpherical(coordinate_2)

    return throw(notification_message.replace("_placeholder_", "radius")) if not objectHasKey(methodConfig, "radius") \
      else ( \
        throw("Provided coordinates are not spherical!") if are_spherical \
        else nSphereDistance(coordinate_1, coordinate_2, methodConfig.radius)
      )

  else:
    throw("There are only available methods: ['n_norm', 'sphere']")
  

'''
  @abstract returns the distance of two points based on
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {String} method
  @param {Object} methodConfig
  @return {Number}
'''
def travelTime( average_speed, coordinate_1, coordinate_2, method, methodConfig): 
    return distance(coordinate_1, coordinate_2, method, methodConfig) / average_speed
