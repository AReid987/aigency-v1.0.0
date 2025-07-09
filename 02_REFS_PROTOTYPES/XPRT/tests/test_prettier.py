#
 # File: test_prettier.py                                                      #
 # Project: devlog-xprt                                                        #
 # Created Date: Sa Apr 2025                                                   #
 # Author: <<author>                                                           #
 # -----                                                                       #
 # Last Modified: Sat Apr 12 2025                                              #
 # Modified By: Antonio J. Reid                                                #
 # -----                                                                       #
 # Copyright (c) 2025 10xAigency                                               #
 # -----                                                                       #
 # HISTORY:                                                                    #
 # Date      	By	Comments                                                   #
 # ----------	---	---------------------------------------------------------  #




import unittest
from packages.xprt-commit.src.xprt_commit.linters.prettier import run_prettier_check

class TestPrettier(unittest.TestCase):
    def test_no_files(self):
        result = run_prettier_check([])
        self.assertEqual(result['needs_formatting'], False)
        self.assertIsNone(result['files'])
        self.assertIsNone(result['error'])
        self.assertEqual(result['stdout'], '')
        self.assertEqual(result['stderr'], '')
        self.assertEqual(result['error'], 'No files provided to run Prettier.')

if __name__ == '__main__':
    unittest.main()
