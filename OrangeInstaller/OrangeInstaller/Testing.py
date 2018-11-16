from Functions import functions, systemTools
import unittest
import sys

class systemToolsTests(unittest.TestCase):
    """
    Class for testing
    """
    
    def test_checkSystemTools(self):
        check = False
        if systemTools.isWindows() == True:
            check=True
            self.assertEqual(sys.platform.startswith("win"), True, "OI.SystemTool for check OS is different to sys method")
        if systemTools.isLinux() == True:
            check=True
            self.assertEqual(sys.platform.startswith("linux"), True, "OI.SystemTool for check OS is different to sys method")
        
        
if __name__ == '__main__':
    unittest.main()