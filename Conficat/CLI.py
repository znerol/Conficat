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
  __DEFAULT_DDIR = "data"
  __DEFAULT_GDIR = os.path.join("tmpl","global")
  __DEFAULT_RDIR = os.path.join("tmpl","row")
  __DEFAULT_ODIR = "out"

  def parse(cls,argv):
    version = "conficat %s" % __version__
    epilog="Tip: if you stick to the default directory layout you don't have"\
      " to supply any options on the command line. Put your csv files into %s"\
      " your row templates into %s and your global templates into %s. If your"\
      " templates generate multiple output files also make sure that the"\
      " default output directory \"%s\" exists." % (CLI.__DEFAULT_DDIR,
      CLI.__DEFAULT_GDIR, CLI.__DEFAULT_RDIR,CLI.__DEFAULT_ODIR)
    parser = OptionParser(version=version,epilog=epilog)

    ingrp = OptionGroup(parser, "Data input","Specify files or directories"\
      " where conficat should look for CSV data. Any of these options may be"\
      " specified multiple times and in any combination. Defaults to --ddir"\
      " %s if this directory exists." % CLI.__DEFAULT_DDIR)
    ingrp.add_option("-d", "--data", dest="csvfiles", action="append",
      help="Load tabular data from csv FILE and store it in the data dictionary"
           " under KEY. If KEY is omitted, the first word of the filename is"
           " used to reference the entry in the data dictionary instead.",
      metavar="[KEY:]FILE", default=[])
    ingrp.add_option("-D", "--ddir", dest="csvdirs", action="append",
      help="Load all csv files from DIR into the data dictionary. Keys are"
           " derived from the filenames.", metavar="DIR", default=[])
    parser.add_option_group(ingrp)

    tplgrp = OptionGroup(parser, "Global template files","Specify files or"
      " directories containing global templates. Every global template will"
      " get called once with the \"data\" dictionary in the cheetah namespace."
      " Any of these options may be specified multiple times and in any"
      " combination. Defaults to --gdir %s if this directory exists." % \
      CLI.__DEFAULT_GDIR)
    tplgrp.add_option("-g", "--glob", dest="gtmplfiles", action="append",
      help="Apply global template in FILE", metavar="FILE", default=[])
    tplgrp.add_option("-G", "--gdir", dest="gtmpldirs", action="append",
      help="Apply all global templates in DIR", metavar="DIR", default=[])
    parser.add_option_group(tplgrp)

    rtplgrp = OptionGroup(parser, "Row template files","Specify files or"
      " directories containing row templates. While looping thru every entry of"
      " the data dictionary conficat looks for a \"template\"-field. If such a"
      " field exists, conficat tries to load the specified template and apply"
      " it with \"data\" and the \"row\" dictionary in the cheetah namespace."
      " Any of these options may be specified multiple times and in any"
      " combination. Defaults to --rdir %s if this directory exists." % \
      CLI.__DEFAULT_RDIR)
    rtplgrp.add_option("-r", "--row", dest="rtmplfiles", action="append",
      help="Add row template to search path", metavar="FILE", default=[])
    rtplgrp.add_option("-R", "--rdir", dest="rtmpldirs", action="append",
      help="Look for row templates in DIR", metavar="DIR", default=[])
    parser.add_option_group(rtplgrp)

    tplgrp = OptionGroup(parser, "Output","Specify the file or a directory"
      " where conficat should put its results. The two options can be combined."
      " If you omit both conficat defaults to --out - (stdout) and --odir %s if"
      " this directory exists." % CLI.__DEFAULT_ODIR)
    tplgrp.add_option("-o", "--out", dest="outfile", default="-",
      help="Write output to FILE", metavar="FILE")
    tplgrp.add_option("-O", "--odir", dest="outdir", metavar="DIR",
      help="Write results of templates calling the \"outfile\" function to DIR")
    parser.add_option_group(tplgrp)

    (opts, args) = parser.parse_args(args=argv)

    # we don't take arguments
    if len(args)>1:
      parser.error("conficat takes no arguments")

    # fallback to default directories if none specified on commad line and if
    # they actually exist.
    if len(opts.csvfiles) == 0 and len(opts.csvdirs) == 0 and \
        os.path.exists(CLI.__DEFAULT_DDIR):
      s=os.stat(CLI.__DEFAULT_DDIR)[ST_MODE]
      if S_ISDIR(s):
        opts.csvdirs.append(CLI.__DEFAULT_DDIR)

    if len(opts.gtmplfiles) == 0 and len(opts.gtmpldirs) == 0 and \
        os.path.exists(CLI.__DEFAULT_GDIR):
      s=os.stat(CLI.__DEFAULT_GDIR)[ST_MODE]
      if S_ISDIR(s):
        opts.gtmpdirs.append(CLI.__DEFAULT_GDIR)

    if len(opts.rtmplfiles) == 0 and len(opts.rtmpldirs) == 0 and \
        os.path.exists(CLI.__DEFAULT_RDIR):
      s=os.stat(CLI.__DEFAULT_RDIR)[ST_MODE]
      if S_ISDIR(s):
        opts.rtmpldirs.append(CLI.__DEFAULT_RDIR)

    if opts.outdir == None and os.path.exists(CLI.__DEFAULT_ODIR):
      s=os.stat(CLI.__DEFAULT_ODIR)[ST_MODE]
      if S_ISDIR(s):
        opts.outdir=CLI.__DEFAULT_ODIR
    
    try:
      ccat=Conficat(
        csvfiles  = opts.csvfiles,
        csvdirs   = opts.csvdirs,
        gtmplfiles= opts.gtmplfiles,
        gtmpldirs = opts.gtmpldirs,
        rtmplfiles= opts.rtmplfiles,
        rtmpldirs = opts.rtmpldirs,
      )
    except ConfigurationError,err:
      parser.error(err)

    return ccat

  parse = classmethod(parse)
