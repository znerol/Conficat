#!/usr/bin/env python
"""
Test cases for conficat utility functions
"""

import unittest
import os
from Conficat.Util import loadCSVPath, autoStripCSVParams
from tempfile import mkstemp, mkdtemp

class LoadCSVPathTestCase(unittest.TestCase):
  """ Test cases for loadCSVPath utility function"""

  csvrec="ID,Name\n1,Marvin\n"
  csvdict=dict(ID="1",Name="Marvin")
  fkey1="listtest"

  def setUp(self):
    self.tmpdir = mkdtemp()
    self.csvfile = os.path.join(self.tmpdir,"%s.csv" % LoadCSVPathTestCase.fkey1)
    f=open(self.csvfile,"w")
    f.write(LoadCSVPathTestCase.csvrec)
    f.close()

  def tearDown(self):
    os.unlink(self.csvfile)
    os.removedirs(self.tmpdir)

  def testValidCSVFile(self):
    """test the structure and content of the resulting dictionary"""

    result1 = {}
    loadCSVPath(self.csvfile,result1,**autoStripCSVParams(self.csvfile))
    self.assertTrue(isinstance(result1,dict))
    self.assertTrue(result1.has_key(LoadCSVPathTestCase.fkey1))

    fkey1list=result1[LoadCSVPathTestCase.fkey1]
    self.assertTrue(isinstance(fkey1list,list))
    self.assertTrue(len(fkey1list)==1)

    fkey1contents=fkey1list[0]
    self.assertTrue(isinstance(fkey1contents,dict))
    self.assertTrue(len(fkey1contents)==len(LoadCSVPathTestCase.csvdict))

    for (key,value) in fkey1contents.iteritems():
      self.assertTrue(LoadCSVPathTestCase.csvdict.has_key(key))
      self.assertEqual(LoadCSVPathTestCase.csvdict[key],value)

if __name__ == '__main__':
  unittest.main()
