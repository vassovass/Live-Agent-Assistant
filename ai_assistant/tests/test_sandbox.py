
import unittest
from utils.sandbox import Sandbox
from utils.error_handler import ErrorHandler
from config.config_loader import ConfigLoader

class TestSandbox(unittest.TestCase):
    def setUp(self):
        config_loader = ConfigLoader()
        self.config = config_loader.config
        self.error_handler = ErrorHandler(self.config)
        self.sandbox = Sandbox(self.config, self.error_handler)

    def test_sandbox_enabled(self):
        code = "x = 5
y = 10
result = x + y"
        self.sandbox.run(code)
        # No exception should be raised

    def test_sandbox_restricted_code(self):
        code = "import os
os.system('echo Hello World')"
        with self.assertRaises(Exception):
            self.sandbox.run(code)

if __name__ == '__main__':
    unittest.main()
