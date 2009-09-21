from ConfigError import ConfigError

class TemplateRegistry(object):

  def __init__(self):
    super(TemplateRegistry, self).__init__()
    self.templates={}

  def __iter__(self):
    for x in self.templates.values():
      yield x

  def __getitem__(self):
    pass

  def addPath(self, path, data, strip=0, prefix=[]):
    tmplext=(lambda p: os.path.basename(p).split(".")[-1].lower() in ("tmpl","py"))
    for f in findfiles(path,tmplext):
      components=prefix+pathexplode(f)[strip:-1]
      key=str.join(".",components)
