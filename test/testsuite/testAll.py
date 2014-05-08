import unittest
import sys
import os

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('.', pattern="*_sveltest.py")
    unittest.TextTestRunner(verbosity=2).run(all_tests)