#!/usr/bin/env python
"""
Conficat main class
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import os
import re
import sys
from Util import loadCSVPath, collectfiles, mapfiles
from TemplateRegistry import TemplateRegistry
from ConfigUtil import checkfilemap, collectuniquefiles
from ConfigError import ConfigError

class Config(object):
  """Conficat configuration class. Refer to CLI.py for an example"""

  def __init__(self):
    super(Config, self).__init__()
    self.data={}
    self.globtmpls=TemplateRegistry()
    self.rowtmpls=TemplateRegistry()

  def addCSVPath(self, path, key=None):
    if key==None:
      loadCSVPath(path,self.data)
    else:
      loadCSVPath(path,self.data,prefix=[key],strip=1)

  def addGlobalTemplatePath(self,path):
    self.globtmpls.addPath(path)

  def addRowTemplatePath(self,path):
    self.rowtmpls.addPath(path)

  def setTemplateColumns(self,tcols=[]):
    self.tmplcols = tcols

  def setOutputFile(self,outf):
    """
    setup either stdout or open a file as a destination for template results
    """
    if outf=="-":
      self.outfile=sys.stdout
    else:
      self.outfile=open(outf,"w")

  def setOutputDir(self,outd):
    """
    specify the directory where additional files created via the outfile def in
    templates should be placed.
    """
    if not os.path.isdir(outd):
      raise ConfigError("%s: Not a directory", outd)
    self.outdir=os.path.normpath(outd)

  def validate(self):
    pass

  def checkfilemap(map, key, path):
    """
    Check a file key against a map (e.g. csvmap, tmplmap, etc). Raises a
    ConfigError if something is wrong with the key (duplicate, invalid)
    """
    if key==None or not re.match(r'^[a-zA-Z0-9_]+$', key):
      raise ConfigError("Invalid key %s for path %s", (key, path))
    if key in map:
      raise ConfigError("Duplicated key %s for path %s", (key, path))

  checkfilemap=staticmethod(checkfilemap)
