#!/usr/bin/env python
"""
Utility functions for conficat
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import csv
import os
import re

def parseCSVFiles(files,*args,**kwds):
  """
  loop thru csv files and build up data-hash. keys are derived from the first
  word of the filename while the contents get stored as values.
  """
  # file parameter must be a dict or list
  assert(isinstance(files,(dict,list)))
  
  # file parameter may not be empty
  assert(len(files)>0)

  # we got a list, derive the keys for the dictionary automatically from the
  # filename.
  fdict={}
  if isinstance(files,list):
    for fpath in files:
      # get rid of special characters in filename and use the result as key in
      # the data directory. i.e. mydata.csv -> mydata:file-contents
      fname = re.split('\W+',os.path.basename(fpath),1)[0]
      if fname==None or fname=="":
        raise Exception("Unable to derive data-key from filename %s" % fpath)

      if fdict.has_key(fname):
        raise Exception("Data-key %s derived from filename %s already exists" % \
            fname, fpath)

      fdict[fname]=fpath
  else:
    fdict=files

  data={}
  for (fname, fpath) in fdict.iteritems():
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
