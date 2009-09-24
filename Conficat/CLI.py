#!/usr/bin/env python
"""
Conficat command line interface
"""

import os
import sys
import logging
from stat import *
from optparse import OptionParser, OptionGroup
from Config import Config
from ConfigError import ConfigError
from Conficat import Conficat


class CLI(object):
  def __init__(self):
    self.loglevel = logging.WARN
    self.logger = logging.getLogger("ccat.cli")

  def opt_loglevel_incr(self, option, opt_str, value, parser, amount):
    self.loglevel=self.loglevel+amount

  def parse(self,argv):
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
    parser = OptionParser(usage=usage)

    parser.add_option("-v", "--verbose", action='callback',
      callback=self.opt_loglevel_incr, callback_args=(-10,),
      help="Increase loglevel. -vv for all debug messages.")

    parser.add_option("-q", "--quiet", action='callback',
      callback=self.opt_loglevel_incr, callback_args=(+10,),
      help="Decrease loglevel. -qq for complete silence.")

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

    # setup logging
    if self.loglevel < logging.DEBUG: self.loglevel=logging.DEBUG
    if self.loglevel > logging.FATAL: self.loglevel=logging.FATAL
    logging.basicConfig(
        level=self.loglevel,
        format='%(levelname).1s:%(message)s',
        stream=sys.stderr
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
      self.logger.error(err)
      exit(2)
    except:
      self.logger.error("An unknown error occured")
      exit(1)

    return ccat
