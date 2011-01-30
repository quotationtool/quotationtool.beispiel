import unittest
import zope.configuration
from zope.component.testing import PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
import quotationtool

import beispiel


class ZCMLTest(PlacelessSetup, unittest.TestCase):

    def testZCML(self):
        self.assertTrue(XMLConfig('configure.zcml', beispiel)() is None)


def test_suite():
    return unittest.TestSuite((
            unittest.makeSuite(ZCMLTest),
            ))
