#!/usr/bin/env python
"""
Conficat template registry module
"""

import re
import os
import sys
from ConfigError import ConfigError
from Util import findfiles, pathexplode
from Cheetah.Template import Template
import logging

class TemplateRegistry(object):
  """
  The TemplateRegistry objects are responsible to load Cheetah and pure python
  templates from files and store them internally for later reference.
  """

  def __init__(self):
    super(TemplateRegistry, self).__init__()
    self.logger=logging.getLogger("ccat.tmpl.reg")
    self.templates={}

  def __iter__(self):
    for (n, t) in self.templates.iteritems():
      yield (n, t)

  def __getitem__(self, key):
    return self.templates[key]

  def __load_py(self, filename, cls=None, basepath=None):
    """
    load a class from a python file
    """
    self.logger.debug("constructing py template from file %s" % filename)
    self.logger.debug("  cls: %s" % cls)
    self.logger.debug("  basepath: %s" % basepath)
    # construct module path from basepath and filename
    pfx = os.path.commonprefix([filename, basepath])
    modpath = filename[len(pfx):]
    # remove leading slash
    modpath = modpath.lstrip(os.path.sep)
    # get rid of file extension
    modpath = re.sub(r'\.[^\.]*$','',modpath)
    components = modpath.split(os.path.sep)
    # create modname and classname
    modname = str.join(".",components)
    if cls == None:
      cls = components[-1]

    self.logger.debug("  trying to import %s from %s" % (cls,modname))
    # try to load the class and return
    exec "from %s import %s as tcls" % (modname, cls)
    self.logger.debug("successfully loaded py template from %s" % f)
    return tcls

  def __template_extension(path):
    """
    Filter for python and cheetah templates
    """
    if os.path.basename(path) == "__init__.py":
      return False
    return re.match(r'.+\.(py|tmpl)$',path.lower()) != None

  __template_extension = staticmethod(__template_extension)

  def addPath(self, path, strip=0, prefix=[]):
    """
    Recursively add cheetah and python templates from path.
    """
    # add base path to python environment
    basedir=os.path.normpath(path)
    if os.path.isfile(path):
      basedir=os.path.dirname(path)
    sys.path.append(basedir)
    self.logger.debug("basedir: %s" % basedir)

    # filter for tmpl and py extensions
    for f in findfiles(path,TemplateRegistry.__template_extension):
      # construct key from filename with path seperators replaced by dots and
      # file extension striped
      components=prefix+pathexplode(f)[strip:-1]
      key=str.join(".",components)
      if self.templates.has_key(key):
        raise ConfigError("%s: duplicate template entry for key %s" % (path,
          key))

      # try to load template class
      ext=f.split(".")[-1].lower()
      self.logger.info("attempting to load template: %s" % f)
      if ext=="tmpl":
        tcls = Template.compile(file=f)
      else: 
        try:
          tcls = self.__load_py(f,basepath=basedir)
        except ImportError,err:
          self.logger.warn("failed to load template: %s" % f)
          continue

      if not issubclass(tcls,Template):
        self.logger.warn("no template class found in: %s" % f)
        continue
      
      # store template class into templates dictionary
      self.templates[key] = tcls
      self.logger.info("successfully loaded template: %s" % f)

    # remove path 
    sys.path.remove(basedir)
