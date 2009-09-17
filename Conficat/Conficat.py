#!/usr/bin/env python
"""
Conficat main class
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

class ConfigurationError(StandardError):
  pass

class Conficat(object):
  def __init__(csvpaths, globtmpls, rowtmpls, tmplcols, outfile, outdir):
    # check paths
    assert(isinstance(csvpaths,list))
    if len(csvpaths) == 0:
      raise ConfigurationError("Please specify at least one input (CSV) file")
    for p in csvpaths:
      pass

  def run(self):
    pass
