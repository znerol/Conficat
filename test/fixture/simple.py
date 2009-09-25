from Cheetah.Template import Template
class simple(Template):
  def __str__(self):
    return "Hello %s\n" % self.getVar("who")
