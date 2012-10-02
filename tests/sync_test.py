import unittest
from mock import MagicMock, call
from cfsync import Sync

class SyncTest(unittest.TestCase):
    def test_clear(self):
        cont = MagicMock(name='mycontainer')
        cont.list_objects.return_value = ['a', 'b', 'c', 'd']
        self.conn.get_container.return_value = cont
        cont.delete_object.mock_calls

        self.sync.clear('mycontainer')

        self.conn.get_container.assert_called_with('mycontainer')
        self.assertEqual(cont.delete_object.mock_calls, [call('a'),call('b'),call('c'),call('d')])

    def setUp(self):
        self.conn = MagicMock()
        self.sync = Sync(self.conn)

    def tearDown(self):
        del self.conn
