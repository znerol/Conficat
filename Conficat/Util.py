#!/usr/bin/env python
"""
Utility functions for conficat
"""

import csv
import os
import re
from stat import *
from ValidationError import ValidationError

def findfiles(path, testfunc=None, recurse=True):
  """
  recurse thru directories until the optional depth.
  """
  assert(isinstance(path,str))
  assert(testfunc==None or callable(testfunc))
  
  path=os.path.normpath(path)
  if S_ISDIR(os.stat(path)[ST_MODE]):
    if recurse == 0:
      return
    if not isinstance(recurse,bool):
      recurse=recurse-1
    for f in os.listdir(path):
      for p in findfiles(os.path.join(path, f), testfunc, recurse):
        yield p
  elif testfunc==None or testfunc(path):
    yield path

def checkrelpath(path):
  """
  ensure that the path is a save relative path: no reference to enclosing dirs
  etc.
  """
  assert(isinstance(path,str))

  p = os.path.normpath(path)
  if p=="":
    raise ValidationError("Empty relative path")
  if p[0:2]=="..":
    raise ValidationError("Reference to enclosing directory (..) not allowed in relative path")
  if p[0]==os.path.sep:
    # FIXME: check for first path character on windows. drive lett
    raise ValidationError("Not a relative path")

  return p
