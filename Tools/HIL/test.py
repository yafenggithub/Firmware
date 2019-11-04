#! /usr/bin/python

import pexpect.fdpexpect
import os, serial, sys, unittest

px4_tests = [
"autodeclination",
"bezier",
"bson",
"commander",
"controllib",
"conv",
"float",
"hrt",
"int",
"IntrusiveQueue",
"List",
"mathlib",
"matrix",
"microbench_hrt",
"microbench_math",
"microbench_matrix",
"microbench_uorb",
"param",
"parameters",
"perf",
"search_min",
"sleep",
"smoothz",
"time",
#"uorb",
"versioning"
]

class TestsCommandSerial(unittest.TestCase):
    def setUp(self):
        self.SERIAL_PORT = os.environ["SERIAL_PORT"]
        self.ser = serial.Serial(self.SERIAL_PORT, 57600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=10)
        self.child = pexpect.fdpexpect.fdspawn(self.ser.fileno(), timeout=10)

def test_generator(cmd):
    def test(self):

        self.child.sendline("tests " + cmd)
        state = self.child.expect([cmd + " FAILED", cmd + " PASSED"], timeout=10)

        #print(self.child.before)

        self.assertNotEqual(state, 0, self.child.before) # FAILED
        self.assertEqual(state, 1, self.child.before) # PASSED

    return test

if __name__ == "__main__":

    for t in px4_tests:
        test_name = 'test_%s' % t
        test = test_generator(t)
        setattr(TestsCommandSerial, test_name, test)

    import xmlrunner

    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'), failfast=False, buffer=False)
    unittest.main()
