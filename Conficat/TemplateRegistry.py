import re
import os
import sys
from ConfigError import ConfigError
from Util import findfiles, pathexplode
from Cheetah.Template import Template

class TemplateRegistry(object):
  """
  The TemplateRegistry objects are responsible to load Cheetah and pure python
  templates from files and store them internally for later reference.
  """
  def __init__(self):
    super(TemplateRegistry, self).__init__()
    self.templates={}

  def __iter__(self):
    for t in self.templates.values():
      yield t

  def __getitem__(self, key):
    return self.templates[key]

  def __load_py(self, filename, cls=None, basepath=None):
    """
    load a class from a python file
    """
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

    # try to load the class and return
    exec "from %s import %s as tcls" % (modname, cls)
    return tcls

  def addPath(self, path, strip=0, prefix=[]):
    """
    Recursively add cheetah and python templates from path.
    """
    # add base path to python environment
    basedir=os.path.normpath(path)
    if os.path.isfile(path):
      basedir=os.path.dirname(path)
    print basedir
    sys.path.append(basedir)

    # filter for tmpl and py extensions
    tmplext=(lambda p: re.match(r'.+\.(py|tmpl)$',p.lower()) != None)
    for f in findfiles(path,tmplext):
      # construct key from filename with path seperators replaced by dots and
      # file extension striped
      components=prefix+pathexplode(f)[strip:-1]
      key=str.join(".",components)
      if self.templates.has_key(key):
        raise ConfigError("%s: duplicate template entry for key %s" % (path,
          key))

      # try to load template class
      ext=f.split(".")[-1].lower()
      if ext=="tmpl":
        tcls = Template.compile(file=f)
      else: 
        tcls = self.__load_py(f,basepath=basedir)

      if not (issubclass(tcls,Template)):
        ConfigError("%s: not a cheetah template" % f)

      # store template class into templates dictionary
      self.templates[key] = tcls

    # remove path 
    sys.path.remove(basedir)
