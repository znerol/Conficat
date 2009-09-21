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

def mapfiles(files):
  """
  Generate a dictionary containing key-value pairs where the key is derived 
  from the first word of the basename from the path in the value part.
  E.g. some/file/there.txt: there -> some/file/there.txt
  """
  for f in files:
    # generate key and yield key-value pair
    key=re.split("\W+", os.path.basename(f), 1)[0]
    yield(key,f)

def collectfiles(path, extensions=None):
  """
  Generate a list of files from a path (file and directory) recursively. Will
  throw OSError if a file or path is not accessible.
  """
  assert(isinstance(path,str))
  assert(isinstance(extensions,(type(None),list)))
  
  path = os.path.normpath(path)
  if S_ISDIR(os.stat(path)[ST_MODE]):
    for f in os.listdir(path):
      for p in collectfiles(os.path.join(path, f), extensions):
        yield p
  else:
    if extensions == None:
      yield path
      return
    try:
      ext = path.rsplit(".",1)[1]
      if ext in extensions:
        yield path
    except IndexError:
      pass


def parseCSVFiles(files,*args,**kwds):
  """
  loop thru csv files and build up data-hash. keys are derived from the first
  word of the filename while the contents get stored as values.
  """

  data={}
  for (fname, fpath) in files.iteritems():
    # read the csv file contents and build up hierarchical dict entries by
    # splitting keys on "." and assigning values as nested entries
    data[fname]=[]
    for row in csv.DictReader(open(fpath,"rb"),*args,**kwds):
      newrow=row.copy()
      for (key,val) in row.iteritems():
        parts = key.split(".")
        if len(parts) == 1:
          continue

        level=newrow
        for part in parts[0:-1]:
          if not level.has_key(part):
            level[part]={}
          level=level[part]
        level[parts[-1]]=val

      data[fname].append(newrow)

  return data
