#!/usr/bin/env python
"""
Conficat internal configuration class
"""

import os
import re
import sys
import logging
from Cheetah.ImportHooks import install as cheetah_import_install
from Util import loadCSVPath, autoStripCSVParams, autoStripTemplateParams
from TemplateRegistry import TemplateRegistry
from ConfigError import ConfigError

class Config(object):
  """Conficat configuration class. Refer to CLI.py for an example"""

  def __init__(self):
    super(Config, self).__init__()
    self.logger=logging.getLogger("ccat.config")
    self.data={}
    self.globtmpls=TemplateRegistry()
    self.rowtmpls=TemplateRegistry()

    # make sure cheetah imports dependant classes automatically
    cheetah_import_install()

  def addCSVPath(self, path, key=None):
    """
    Add a file or directory containing tabular data in CSV format
    """
    kwa=autoStripCSVParams(path, key)
    loadCSVPath(path, self.data, **kwa)

  def addGlobalTemplatePath(self,path):
    """
    Add a file or directory path containing global templates
    """
    self.logger.info("adding global template(s) in \"%s\"" % path)
    kwa=autoStripTemplateParams(path)
    self.globtmpls.addPath(path, **kwa)

  def addRowTemplatePath(self,path):
    """
    Add a file or directory path containing row templates
    """
    self.logger.info("adding row template(s) in \"%s\"" % path)
    kwa=autoStripTemplateParams(path)
    self.rowtmpls.addPath(path, **kwa)

  def setTemplateColumns(self,tcols=[]):
    """
    Set the names of the columns which may contain a reference to a row
    template
    """
    self.logger.info("columns for row templates: %s" % ", ".join(tcols))
    self.tmplcols = tcols

  def setOutputFile(self,outf):
    """
    Setup either stdout or open a file as a destination for template results
    """
    if outf=="-":
      self.logger.info("write output to stdout")
      self.outfile=sys.stdout
    else:
      self.logger.info("write output to file %s" % outf)
      self.outfile=open(outf,"w")

  def setOutputDir(self,outd):
    """
    Specify the directory where additional files created via the outfile def in
    templates should be placed.
    """
    if not os.path.isdir(outd):
      raise ConfigError("%s: Not a directory" % outd)
    self.outdir=os.path.normpath(outd)
    self.logger.info("write separate output files to directory %s" % outd)

  def validate(self):
    """
    Validate the configuration
    """
    # FIXME
    pass
