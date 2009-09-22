#!/usr/bin/env python
"""
Conficat command line interface
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import os
import sys
import logging
from stat import *
from optparse import OptionParser, OptionGroup
from Config import Config
from ConfigError import ConfigError
from Conficat import Conficat

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

    parser.add_option("-d", "--debug", dest="dlevel", default=logging.DEBUG,
      help="Set logging level", metavar="LEVEL")

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

    # parse arguments
    (opts, args) = parser.parse_args(args=argv)

    # setup logging and general exception handler
    logging.basicConfig(
        level=opts.dlevel,
        format=logging.BASIC_FORMAT,
        stream=sys.stdout
    )

    if len(opts.tcols) == 0:
      opts.tcols.append("template")
    
    try:
      config=Config()

      # handle command line arguments
      # split out arguments with key= prefix
      for arg in args[1:]:
        try:
          (key,path)=arg.split("=",1)
          config.addCSVPath(path,key)
        except ValueError:
          # we get here if python is unable to unpack enough elements from
          # split, which means we have to figure out the key ourselves and
          # recurse into subdirectories
          config.addCSVPath(arg)

      # handle options
      for path in opts.gtmpl:
        config.addGlobalTemplatePath(path)

      for path in opts.rtmpl:
        config.addRowTemplatePath(path)

      config.setTemplateColumns(opts.tcols)
      config.setOutputFile(opts.outfile)
      if opts.outdir:
        config.setOutputDir(opts.outdir)

      # check configuration
      config.validate()

      ccat=Conficat(config)
    except ConfigError,err:
      parser.error(err)

    return ccat

  parse = classmethod(parse)
