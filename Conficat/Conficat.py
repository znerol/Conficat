#!/usr/bin/env python
"""
Conficat main class
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

from stat import *
from Util import parseCSVFiles, collectfiles, mapfiles
import os
import re

class ConfigurationError(StandardError):
  pass

class Conficat(object):
  """Conficat main class. Refer to CLI.py for an example"""

  def __init__(self, csvpaths=[], csvmap={}, globtmpls=[], rowtmpls=[],
      tmplcols=[], outfile=None, outdir=None):

    # check parameters
    assert(isinstance(csvpaths,list))
    assert(isinstance(csvmap,dict))
    assert(isinstance(globtmpls,list))
    assert(isinstance(rowtmpls,list))
    assert(isinstance(tmplcols,list))
    assert(isinstance(outfile,(type(None),str)))
    assert(isinstance(outdir,(type(None),str)))

    # we need at least one csv file ...
    if len(csvpaths) == 0 and len(csvmap) == 0:
      raise ConfigurationError("Please specify at least one input (CSV) file")

    # ... and at least one template
    if len(globtmpls) == 0 and len(rowtmpls) == 0:
      raise ConfigurationError("Please specify at least one template file")

    # collect csv files from csvpaths and generate keys for them
    try:
      for p in csvpaths:
        for (key,f) in mapfiles(collectfiles(p,["csv","CSV"])):
          Conficat.checkfilemap(csvmap, key, path)
          csvmap[key]=f
    except OSError, (errno, message):
      raise ConfigurationError("%s: %s (%d)", f, message, errno)

    # read csv data
    self.data=parseCSVFiles(csvmap)
    print self.data

    # build up template classes
    self.rowtmpls={}
    self.globtmpls={}
    for (tmpl, paths) in ((self.rowtmpls, rowtmpls), (self.globtmpls, globtmpls)):
      # If path is a directory, add it to sys.path. 
      for p in paths:
        for (key, f) in mapfiles(collectfiles(p,["tmpl","py"])):
          Conficat.checkfilemap(tmpl, key, p)
          tmpl[key]=f

  def checkfilemap(map, key, path):
    """
    Check a file key against a map (e.g. csvmap, tmplmap, etc). Raises a
    ConfigurationError if something is wrong with the key (duplicate, invalid)
    """
    if key==None or key=="":
      raise ConfigurationError("Invalid key %s for path %s", (key, path))
    if map.has_key(key):
      raise ConfigurationError("Duplicated key %s for path %s", (key, path))

  checkfilemap=staticmethod(checkfilemap)
  
  def run(self):
    pass
