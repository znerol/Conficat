#!/usr/bin/env python
"""
Conficat internal configuration class
"""

import os
import re
import sys
import logging
from Cheetah.ImportHooks import install as cheetah_import_install
from TemplateRegistry import TemplateRegistry
from CSVDataSource import CSVDataSource
from ConfigError import ConfigError

class Config(object):
  """Conficat configuration class. Refer to CLI.py for an example"""

  def __init__(self):
    super(Config, self).__init__()
    self.logger=logging.getLogger("ccat.config")
    self.data = CSVDataSource()
    self.globtmpls=TemplateRegistry()
    self.rowtmpls=TemplateRegistry()

    # make sure cheetah imports dependant classes automatically
    cheetah_import_install()

  def addCSVPath(self, path, key=None):
    """
    Add a file or directory containing tabular data in CSV format
    """
    self.data.loadFromPath(path)

  def addGlobalTemplatePath(self,path):
    """
    Add a file or directory path containing global templates
    """
    self.logger.info("adding global template(s) in \"%s\"" % path)
    self.globtmpls.addPath(path)

  def addRowTemplatePath(self,path):
    """
    Add a file or directory path containing row templates
    """
    self.logger.info("adding row template(s) in \"%s\"" % path)
    self.rowtmpls.addPath(path)

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
    if len(self.data) == 0:
      self.logger.warn("No data was loaded from any csv file")

    # check templates and data
    while True:
      # Operation with only one global template is possible
      if len(self.globtmpls) > 0:
        break

      # Operation with some datasource and some row templates is possible
      if len(self.data) > 0 or len(self.rowtmpls) > 0:
        break

      # Without anything we can do nothing
      raise ConfigError("Either at least one global template and/or some data and at least one row template is required.")

    # check template columns if row templates specified
    if len(self.rowtmpls) > 0 and len(self.tmplcols) == 0:
      raise ConfigError("Row templates specified but no template columns.")
