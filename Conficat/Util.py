#!/usr/bin/env python
"""
Utility functions for conficat
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import csv
import os
import re
from stat import *

def findfiles(path, testfunc=None, recurse=True):
  """
  recurse thru directories until the optional depth.
  """
  assert(isinstance(path,str))
  assert(callable(testfunc))
  
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

def pathexplode(path):
  """
  split file path into components.
  """
  # remove leading dots and slashes
  base = path.lstrip("/.",)
  # split basename into base ext. This will throw a ValueError if the file
  # does not have an extension or there is more than one dot
  (base, ext) = base.split(".")
  return base.split(os.path.sep) + [ext]

def loadCSVPath(path,data,strip=0,prefix=[],*args,**kwds):
  """
  Load CSV data from the path which is either a file or a whole directory.
  """
  assert(path,str)
  assert(data,dict)
  assert(prefix,list)
  assert(strip,int)

  csvext=(lambda p: os.path.basename(p).split(".")[-1].lower() in ("csv",))
  for f in findfiles(path,csvext):
    components=prefix+pathexplode(f)[strip:-1]
    leaf=data

    # descend to leaf
    for c in components[0:-1]:
      if not leaf.has_key(c):
        leaf[c]={}
      leaf=leaf[c]

    # copy rows
    leaf[components[-1]]=[]
    for row in csv.DictReader(open(f,"rb"),*args,**kwds):
      newrow={}
      for (key,val) in row.iteritems():
        parts = key.split(".")
        if len(parts) == 1:
          newrow[key]=val
          continue

        level=newrow
        for part in parts[0:-1]:
          if not level.has_key(part):
            level[part]={}
          level=level[part]
        level[parts[-1]]=val

      leaf[components[-1]].append(newrow)

def autoStripParams(path, rename=None):
  """
  automatically create 'strip' and 'prefix' parameters by removing all leading path
  components but the last one and applying 'key' to 'prefix' if requested.
  """
  kwa={}
  strip=len(os.path.normpath(path).lstrip("/.").split(os.path.sep))-1

  if rename!=None:
    kwa['prefix']=[rename]
    strip=strip+1

  kwa['strip']=strip
  return kwa

