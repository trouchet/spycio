from math import pi
from numpy import sin, cos
from functools import reduce

'''
  @abstract raise an error message 
 
  @param {string} message
  @param {Object} errorClass 
  @return
'''
def throw(message, errorClass=Exception):
  raise errorClass(message)

'''
  @abstract JSON object has $key string among keys
 
 
  @param {Object} object
  @param {String} key
  @return {Object}
'''
def hasKey(object, key):
  return key in object.keys()

'''
  @abstract converts randian to degree angle
 
  @param {Number} radian_angle
  @return {NUmber}
'''
def radianToDegree(angle_radian): 
  return (180 * angle_radian) / pi

'''
  @abstract converts degree to randian angle
 
  @param {Number} radian_angle
  @return {Number}
'''
def degreeToRadian(angle_degree): 
  return (pi * angle_degree) / 180

'''
  @abstract return haversine function sin^2(theta)
 
  @param {Number} radian_angle
  @return {NUmber}
'''
def hav(theta_radian): 
  return sin(theta_radian / 2) ** 2

'''
  @abstract convert geographical coordinates a.k.a. 
  latitude and longitude in degrees, into spherical coordinates
 
  @param {Number} lat_degree
  @param {Number} lng_degree
  @return {Number}
'''
def geoToSpher(lat_degree, lng_degree):
  return [pi/2 + degreeToRadian(lat_degree), pi + degreeToRadian(lng_degree)]

'''
  @abstract convert spherical coordinates into 
  geographical coordinates a.k.a. latitude and longitude in degrees
 
  @param {Number} lat_degree
  @param {Number} lng_degree
  @return {Number}
'''
def spherToGeo(coordinates):
  return radianToDegree(coordinates[0]-pi/2), radianToDegree(coordinates[1]-pi)


'''
  @abstract an geographical coordinate of dimension n has:
   1. Dimension equal 2;
   2. Entries from index:
     a. first entry  (latitude)  : between [-pi/2, pi/2];
     b. second entry (longitude) : between [  -pi, pi];
 
  @param {Array} u
  @return {Boolean}
'''
def isGeographical(u):
  def hasLength2(x):
    return (len(x) == 2)
  def isBetweenmmPI2andpPI2(vec):
    return (vec[0] >= -90 and vec[0] <= 90)
  def isBetweenmPIandpPI(vec):
    return (vec[1] >= -180 and vec[1] <= 180)
  
  return hasLength2(u) and isBetweenmmPI2andpPI2(u) and isBetweenmPIandpPI(u)

'''
  @abstract an spherical coordinate of dimension n has:
   1. Dimension greater than 2;
   2. Entries from index:
     a. 0 to indexn-2 : between [-pi, pi];
     b. indexn-1      : between [0, 2 pi];
 
  @param {Array} u
  @return {Boolean}
'''
def isSpherical(u):
  u_length=len(u)

  def isBetween0andpPI(result, elem):
    return (result and elem >= 0 and elem <= pi)
  def isBetween0and2PI(result, elem):
    return (result and elem >= 0 and elem <= 2 * pi)
  
  def areBetweenmPIandpPI(vec):
    return reduce(isBetween0andpPI, vec, True)
  def areBetween0and2PI(vec):
    return reduce(isBetween0and2PI, vec, True)

  return u_length >= 2 and \
    areBetweenmPIandpPI(u[0:u_length - 1]) and\
    areBetween0and2PI(u[u_length - 1:u_length])

'''
  @abstract converts map of spherical to cartesian coordinates
  The 3D representation order corresponds to (z, x, y)
 
  @param {boolean} a
  @param {boolean} b
  @return {boolean}
'''
def spherToCart(coords, R):
  len_coords=len(coords)
  
  if(isSpherical(coords)):
    
    def prodsin(angles): 
      def sinprodFun(prod_sofar, angle):
        return (prod_sofar * sin(angle))
      return 1 if len(angles) == 0 else reduce(sinprodFun, angles, 1)

    def s2cRecur(angles, index):
      return prodsin(angles[0:index]) * cos(angles[index])
    
    prev_coords = coords[0:len_coords - 1]
    indexes = range(len_coords)
    curr_coord = coords[len_coords - 1]
    last_coord = [R * prodsin(prev_coords) * sin(curr_coord)]
    
    def spherDistFun(index):
      return (R * s2cRecur(coords, index))  
    
    prev_sphers=list(map(spherDistFun, indexes))
    prev_sphers.extend(last_coord)

    return prev_sphers
  
  else: 
    criterium_1='1. It is an array with more than two elements;'
    criterium_2='2. Elements between indexes {0} to {1} must be between -pi and pi;'.format(\
      0, len_coords - 1
    )
    criterium_3='3. Last element must be between 0 and 2*pi.'

    emsg='These are criteria for input to be spherical: \n{criteria[0]}\n {criteria[1]} \n'.format(\
      criteria=[criterium_1, criterium_2, criterium_3] \
    )
    
    throw(emsg, TypeError)
