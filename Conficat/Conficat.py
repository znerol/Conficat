#!/usr/bin/env python
"""
Conficat main class
"""

import logging
import os
from Config import Config
from Util import checkrelpath

class Conficat(object):
  """Conficat main class. Refer to CLI.py for an example"""

  def __init__(self, config):
    # check parameters
    assert(isinstance(config, Config))
    self.logger=logging.getLogger("ccat.main")
    self.config = config

  def templates(self):
    """
    Generate instances of templates
    """
    # global templates
    for (tname, tcls) in self.config.globtmpls:
      self.logger.debug("attempting to apply global template %s", tname)
      t=tcls(namespaces={'data':self.config.data})
      yield t
      self.logger.debug("successfully applied global template %s", tname)

    # row templates
    for (key, rows) in self.config.data:
      for row in rows:
        for tmplcol in filter(lambda x: x in self.config.tmplcols, row.keys()):
          self.logger.debug("attempting to apply row template %s", tmplcol)
          tcls=self.config.rowtmpls[row[tmplcol]]
          t=tcls(namespaces={'data':self.config.data, 'row':row})
          yield t
          self.logger.debug("successfully applied row template %s", tmplcol)

  def run(self):
    """
    Loop thru templates, choose output file and apply them.
    """
    for t in self.templates():
      outf = self.config.outfile
      closef = False
      if hasattr(t, "outfile") and callable(t.outfile):
        outpath=t.outfile()
        outpath=checkrelpath(outpath)

        # automatically create enclosing directories
        outdir = os.path.join(self.config.outdir, os.path.dirname(outpath))
        if not os.path.exists(outdir):
          os.makedirs(outdir)

        # open file object
        outf = open(os.path.join(outdir,os.path.basename(outpath)), "w")
        closef = True

      # apply template and write it to the choosen file
      outf.write(str(t))

      if closef:
        outf.close()
