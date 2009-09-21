#!/usr/bin/env python
"""
Conficat main class
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import os
import re
import sys
from Util import loadCSVPath, autoStripParams
from TemplateRegistry import TemplateRegistry
from ConfigError import ConfigError

class Config(object):
  """Conficat configuration class. Refer to CLI.py for an example"""

  def __init__(self):
    super(Config, self).__init__()
    self.data={}
    self.globtmpls=TemplateRegistry()
    self.rowtmpls=TemplateRegistry()

  def addCSVPath(self, path, key=None):
    kwa=autoStripParams(path, key)
    loadCSVPath(path, self.data, **kwa)

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
