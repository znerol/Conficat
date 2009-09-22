#!/usr/bin/env python
"""
Conficat main class
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import logging
from Config import Config

class Conficat(object):
  """Conficat main class. Refer to CLI.py for an example"""

  def __init__(self, config):
    # check parameters
    assert(isinstance(config, Config))
    self.logger=logging.getLogger("ccat.run")
    self.config = config


  def run(self):
    """
    Loop thru and apply global templates, loop thru data and apply rows. Output
    is written to the file / directory configured in __init__
    """
    # global templates
    for (tname, tcls) in self.config.globtmpls:
      self.logger.debug("attempting to apply global template %s", tname)
      t=tcls(namespaces={'data':self.config.data})
      print t
      self.logger.debug("successfully applied global template %s", tname)

    # row templates
    for (key, rows) in self.config.data.iteritems():
      for row in rows:
        for tmplcol in filter(lambda x: x in self.config.tmplcols, row.keys()):
          self.logger.debug("attempting to apply row template %s", tmplcol)
          tcls=self.config.rowtmpls[row[tmplcol]]
          t=tcls(namespaces={'data':self.config.data, 'row':row})
          # FIXME: handle output
          self.logger.debug("successfully applied row template %s", tmplcol)
          print t
