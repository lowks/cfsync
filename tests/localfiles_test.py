import unittest
from mock import patch
from cfsync import Sync

test_walk = [
['.', ['sub1', 'sub2'], ['a.1', 'b.1', 'c.1']],
['./sub1', ['sub3'], ['a.file']],
['./sub2', [], ['a.2', 'b.2', 'c.2']],
['./sub1/sub3', [], ['a.3', 'b.3', 'c.3', 'd.3']]
]

class SyncTest(unittest.TestCase):
    """
    Test that cfsync usage helpers.
    """

    @patch('os.walk', return_value=iter(test_walk))
    def test_listing_files(self, mockwalk):
        """
        Check that that the file tree is walked
        """
        results = [
        './a.1', './b.1', './c.1',
        './sub1/a.file',
        './sub2/a.2', './sub2/b.2', './sub2/c.2',
        './sub1/sub3/a.3', './sub1/sub3/b.3', './sub1/sub3/c.3', './sub1/sub3/d.3'
        ]
        self.assertEqual(self.CFSync.list_files('.'), results)

    def setUp(self):
        self.CFSync = Sync

    def tearDown(self):
        del self.CFSync
