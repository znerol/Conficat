#!/usr/bin/env python
"""
Conficat main class
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

from stat import *
import os

class ConfigurationError(StandardError):
  pass

class Conficat(object):
  """Conficat main class. Refer to CLI.py for an example"""

  def __checkpath(self, path):
    try:
      mode = os.stat(path)[ST_MODE]
    except OSError,(errno,errmsg):
      raise ConfigurationError("Failed to access path %s: %s (%d)", path,
              errmsg, errno)
    return (S_ISDIR(mode), os.path.normpath(path))

  def __collectfiles(self, pathlist=[], extensions=[]):
    results=[]
    print pathlist
    for p in pathlist:
      (isdir, p) = self.__checkpath(p)
      if isdir:
        flist=[]
        for ext in extensions:
          flist.extend(glob.glob("%s/*.%s" % (f, ext)))
        for f in flist:
          (tname,ext) = os.path.basename(f).split(".")
          globtemplates.append((f,tname,ext))
      else:
        (tname,ext) = os.path.basename(p).split(".")
        globtemplates.append((f,tname,ext))

  def __init__(self, csvpaths=[], globtmpls=[], rowtmpls=[], tmplcols=[],
      outfile=None, outdir=None):
    # check csv paths
    assert(isinstance(csvpaths,list))
    if len(csvpaths) == 0:
      raise ConfigurationError("Please specify at least one input (CSV) file")

    datafiles=self.__collectfiles(csvpaths, ["csv"])
    if len(datafiles) == 0:
      raise ConfigurationError("No csvfiles found in specified path(s)")

    # check if we have at least one template path
    if len(globtmpls) == 0 and len(rowtmpls):
      raise ConfigurationError("Please specify at least one template file")

    # check global templates
    # build array containing tuples ("tmpl"|"py","classname","path")
    assert(isinstance(globtmpls,list))
    globtemplates=self.__collectfiles(cvspaths, ["py","tmpl"])

    # check row templates
    # build array containing tuples ("tmpl"|"py","classname","path")
    assert(isinstance(rowtmpls,list))
    rowtemplates=self.__collectfiles(cvspaths, ["py","tmpl"])

    if len(globtemplates) == 0 and len(rowtemplates):
      raise ConfigurationError("No template files found in specified path(s)")

  def run(self):
    pass
