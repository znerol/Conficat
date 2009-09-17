#!/usr/bin/env python
"""
Conficat command line interface
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import os
from stat import *
from optparse import OptionParser, OptionGroup
from Conficat import Conficat, ConfigurationError

class CLI(object):
  def parse(cls,argv):
    version = "conficat %s" % __version__
    usage = """%prog [options] [[key=]file.cvs|dir]...

CSV data files:
  Conficat parses each CSV file specified on the command line and makes its
  contents available in the "$data" placeholder for further usage in cheetah
  templates. If no optional "key" is specified the first word of the filename
  will be used as the key in the data dictionary. Also if you specify a
  directory on the command line it will create an entry for each CSV file found
  in that directory.

Global templates:
  Conficat calls each specified global template with the populated "$data"
  placeholder.

Row templates:
  For each row of every file loaded into the data dictionary conficat tries
  to load the templates refered to in the "template"-column(s). Those are
  called with the "$data"- and additionally a "$row" placeholder populated
  with the values from the current row.
    """
    parser = OptionParser(version=version,usage=usage)

    parser.add_option("-g", "--global", dest="gtmpl", action="append",
      help="Call global template from FILE or every template in DIR. This"
           " option may be specified multiple times.",
           metavar="FILE|DIR", default=[])

    parser.add_option("-r", "--row", dest="rtmpl", action="append",
      help="Add row template form FILE or every template in DIR to the search"
           " path for row templates. This option may be specified multiple."
           " times.", metavar="FILE|DIR", default=[])

    parser.add_option("-c", "--col", dest="tcols", action="append", default=[],
      help="Names of columns referring to row templates. Default: template.")

    parser.add_option("-o", "--out", dest="outfile", default="-",
      help="Write output to FILE.", metavar="FILE")

    parser.add_option("-O", "--odir", dest="outdir", metavar="DIR",
      help="Write generated files of templates calling the \"outfile\" function"
           " to DIR.")

    (opts, args) = parser.parse_args(args=argv)

    if len(opts.tcols) == 0:
      opts.tcols.append("template")

    try:
      ccat=Conficat(
          csvpaths  = args,
          globtmpls = opts.gtmpl,
          rowtmpls  = opts.rtmpl,
          tmplcols  = opts.tcols,
          outfile   = opts.outfile,
          outdir    = opts.outdir
      )
    except ConfigurationError,err:
      parser.error(err)

    return ccat

  parse = classmethod(parse)
