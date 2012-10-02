import unittest
from cfsync.md5sum import md5sum

class MD5SumTest(unittest.TestCase):
    """
    Test that cfsync usage helpers.
    """

    def test_listing_files(self ):
        EXPECTED_MD5 = 'a2a8674cec36a2ebbc689f2ff537c34b'
        self.assertEqual(md5sum('tests/fixtures/somefile.txt'), EXPECTED_MD5)
