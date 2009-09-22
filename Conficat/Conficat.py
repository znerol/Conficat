#!/usr/bin/env python
"""
Conficat main class
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

from Config import Config

class Conficat(object):
  """Conficat main class. Refer to CLI.py for an example"""

  def __init__(self, config):
    # check parameters
    assert(isinstance(config, Config))
    self.config = config


  def run(self):
    """
    Loop thru and apply global templates, loop thru data and apply rows. Output
    is written to the file / directory configured in __init__
    """
    # global templates
    for (tname, t) in self.config.globtmpls:
      t.apply(self.config.outfile, self.config.outdir,
          namespaces={'data':self.config.data})

    # row templates
    for (key, rows) in self.config.data.iteritems():
      for row in rows:
        for tmplcol in filter(lambda x: x in self.config.tmplcols, row.keys()):
          tcls=self.config.rowtmpls[row[tmplcol]]
          t=tcls(namespaces={'data':self.config.data, 'row':row})
          # FIXME: handle output
          print t
