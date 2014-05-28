#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Define 1D quantities. A 1D quantity is represented by (x, y)-value pairs,
which are stored two 1D arrays. Whenever an arithmetic operation between two
such quantity objects is requested, the discretizations are merged and linear
interpolation is used.

Please note that only the most basic arithmetic operations are implemented
right now."""
__created__  = '2012-04-23'
__modified__ = '2012-06-27'
import numpy, scipy.interpolate



class Quantity(object):
  """Define a 1D quantity."""
  __created__  = '2012-04-23'
  __modified__ = '2012-06-22'
  ### add sequence-like interface (behave like a list of x-y pairs)
  ### especially add an "append" method

  def __init__(self, x, y):
    """Initialize 1D quantity."""
    # 2012-04-23

    # force Numpy arrays
    x, y = numpy.array(x), numpy.array(y)

    # check data dimensions
    if len(x.shape) != 1 or len(y.shape) != 1:
      raise ValueError, 'incorrect data shape'

    # sort x- and y-data by x, so that x is monotonically increasing
    ind = numpy.argsort(x)
    x, y = x[ind], y[ind]

    # store data
    self.x = x
    self.y = y

  def interp(self, kind='linear'):
    """Return interpolation object of the quantity."""
    # 2012-04-23
    return scipy.interpolate.interp1d(self.x, self.y, copy=False, kind=kind)

  def value(self, x, kind='linear'):
    """Get the value of the quantity at any given position x. Interpolate if
    needed. Error if x is out of range."""
    # 2012-04-23
    return float(self.interp(kind=kind)(x))

  def commonx(self, other):
    """Merge discretizations of this quantity and the other."""
    # 2012-04-23

    # determine extremal values
    min1, max1 = min(self.x), max(self.x)
    min2, max2 = min(other.x), max(other.x)
    newmin = max(min1, min2)
    newmax = min(max1, max2)

    # choose coarsest discretization ## is there a better way?
    cand1 = self.x[numpy.logical_and(self.x >= newmin, self.x <= newmax)]
    cand2 = other.x[numpy.logical_and(other.x >= newmin, other.x <= newmax)]
    return cand1 if len(cand1) <= len(cand2) else cand2

  def __div__(self, other):
    __created__  = '2012-04-23'
    __modified__ = '2012-06-22'
    if type(other) is type(self):
      x = self.commonx(other)
      y = self.interp()(x)/other.interp()(x)
      return Quantity(x=x, y=y)
    else:
      # assume scalar operation
      return Quantity(x=self.x, y=self.y/other)

  def __add__(self, other):
    __created__  = '2012-04-23'
    __modified__ = '2012-06-22'
    if type(other) is type(self):
      x = self.commonx(other)
      y = self.interp()(x)+other.interp()(x)
      return Quantity(x=x, y=y)
    else:
      # assume scalar operation
      return Quantity(x=self.x, y=self.y+other)

  def __sub__(self, other):
    __created__  = '2012-04-23'
    __modified__ = '2012-06-22'
    if type(other) is type(self):
      x = self.commonx(other)
      y = self.interp()(x)-other.interp()(x)
      return Quantity(x=x, y=y)
    else:
      # assume scalar operation
      return Quantity(x=self.x, y=self.y-other)

  def __mul__(self, other):
    __created__  = '2012-04-23'
    __modified__ = '2012-06-22'
    if type(other) is type(self):
      x = self.commonx(other)
      y = self.interp()(x)*other.interp()(x)
      return Quantity(x=x, y=y)
    else:
      # assume scalar operation
      return Quantity(x=self.x, y=self.y*other)

  def __pow__(self, other):
    __created__  = '2012-04-23'
    __modified__ = '2012-06-22'
    if type(other) is type(self):
      x = self.commonx(other)
      y = self.interp()(x)**other.interp()(x)
      return Quantity(x=x, y=y)
    else:
      # assume scalar operation
      return Quantity(x=self.x, y=self.y**other)

  def __repr__(self):
    """Return string representation."""
    # 2012-04-23
    return '%s(%s, %s)' % (self.__class__.__name__,
                           repr(list(self.x)),
                           repr(list(self.y)))


