#!/usr/bin/env python
"""
Test cases for TemplateRegistry class
"""

import unittest
import os
import logging
import sys
from Cheetah.Template import Template
from Conficat.TemplateRegistry import TemplateRegistry
from tempfile import mkstemp, mkdtemp



class TemplateRegistryTestCase(unittest.TestCase):
  """ Test cases for TemplateRegistry class"""

  def setUp(self):
    # data
    self.tname="simple"
    self.tns={"who":"TestRunner"}

    # test instance
    self.tr = TemplateRegistry()

    # path to fixtures:
    self.fixpath = os.path.join(os.path.dirname(__file__),"fixture")

  def tearDown(self):
    pass

  def testValidSimpleTemplateFile(self):
    """Test the structure and content of a single cheetah template"""

    # load template
    self.tr.loadFromPath(os.path.join(self.fixpath,"%s.tmpl" % self.tname))
    self.assertTrue(self.tname in self.tr)

    # check template class
    tcls=self.tr[self.tname]
    self.assertTrue(issubclass(tcls,Template))

    # check generated content
    tmpl = tcls(namespaces=self.tns)
    ef = open(os.path.join(self.fixpath,"%s.out" % self.tname))
    self.assertEqual(str(tmpl), ef.read())
    ef.close()

  def testValidSimplePythonFile(self):
    """Test the structure and content of a single python template"""

    # load template
    self.tr.loadFromPath(os.path.join(self.fixpath,"%s.py" % self.tname))
    self.assertTrue(self.tname in self.tr)

    # check template class
    tcls=self.tr[self.tname]
    self.assertTrue(issubclass(tcls,Template))

    # check generated content
    tmpl = tcls(namespaces=self.tns)
    ef = open(os.path.join(self.fixpath,"%s.out" % self.tname))
    self.assertEqual(str(tmpl), ef.read())
    ef.close()

if __name__ == '__main__':
  unittest.main()
