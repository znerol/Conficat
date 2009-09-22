import re
import os
import sys
from ConfigError import ConfigError
from Util import findfiles, pathexplode

class TemplateRegistry(object):

  def __init__(self):
    super(TemplateRegistry, self).__init__()
    self.templates={}

  def __iter__(self):
    for t in self.templates.values():
      yield t

  def __getitem__(self, key):
    return self.template[key]

  def addPath(self, path, strip=0, prefix=[]):
    """
    Recursively add cheetah and python templates from path.
    """
    # add base path to python environment
    basedir=os.path.normpath(path)
    if os.path.isfile(path):
      basedir=os.path.dirname(dir)
    sys.path.append(basedir)

    # filter for tmpl and py extensions
    tmplext=(lambda p: re.match(r'.+\.(py|tmpl)$',p.lower()) != None)

    for f in findfiles(path,tmplext):
      # construct key from filename with path seperators replaced by dots and
      # file extension striped
      components=prefix+pathexplode(f)[strip:-1]
      key=str.join(".",components)
      if self.templates.has_key(key):
        raise ConfigError("%s: duplicate template entry for key %s" % (path, key))

      # try to load template class
      ext=f.split(".")[-1].lower()
      if ext=="tmpl":
        tcls = Template.compile(file=f)
      else: 
        # remove leading directory component
        tmodname = f[len(basedir)+1:].replace(os.path.sep,".")
        tmodname = str.join(".",tmodname.split(".")[0:-1])
        tclsname = tmodname.rsplit(".",1)[0]
        print tmodname, tclsname
        try:
          exec "from %s import %s as tcls" % (tmodname,tclsname)
        except ImportError:
          raise

      # store template class into templates dictionary
      self.templates[key] = tcls

    # remove path 
    sys.path.remove(basedir)
