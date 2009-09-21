from ConfigUtil import collectuniquefiles
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

  def addPath(self, path):
    for (f, base, ext) in collectuniquefiles(self.templates.keys(), path,
        ["tmpl","py"]):
      pass
