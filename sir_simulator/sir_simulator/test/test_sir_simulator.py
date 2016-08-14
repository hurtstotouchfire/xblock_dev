import unittest

from mock import Mock

from xblock.test.tools import TestRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from sir_simulator.sir_simulator import SIRSimulatorXBlock

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class SIRSimulatorXBlock(unittest.TestCase):

    def test_default_values_of_fields(self):
        key_store = DictKeyValueStore()
        field_data = KvsFieldData(key_store)
        runtime = TestRuntime(services={'field-data': field_data})
        test_xblock = SIRSimulatorXBlock(runtime)
        
        assertEqual(test_xblock.description, '')

if __name__ == '__main__':
    unittest.main()
