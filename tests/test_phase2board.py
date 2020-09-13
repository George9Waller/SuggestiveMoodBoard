import unittest
import os
from peewee import *

import app
from models import User, Board
from tests.test_auth import UserModelTestCase

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect(reuse_if_open=True)
TEST_DB.create_tables([User, Board], safe=True)


class BoardHelperTestCase(UserModelTestCase):
    """Helper functions"""
    def newboard(self):
        self.register()
        self.login('un', 'P&ssw0rd')
        self.app.post('/add-board',
                      data=dict(name="TestBoard", venuesize="Small", eventdate="2020-09-20"),
                      follow_redirects=True)


class GetPagesTestCase(BoardHelperTestCase):
    """Performs get requests on all new pages"""
    def test_index_page(self):
        rv = self.app.get('/', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_add_board(self):
        rv = self.app.get('/add-board', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_view_board(self):
        self.newboard()
        rv = self.app.get('/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_delete_board(self):
        self.newboard()
        rv = self.app.get('/delete/board/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)


class PostPagesTestCase(BoardHelperTestCase):
    """Performs post requests on new forms"""
    def test_add_valid_board(self):
        self.register()
        self.login('un', 'P&ssw0rd')
        rv = self.app.post('/add-board',
                           data=dict(name="TestBoard", venuesize="Small", eventdate="2020-09-20"),
                           follow_redirects=True)
        self.assertIn(b'Board Added', rv.data)

    def test_delete_valid_board(self):
        self.newboard()
        rv = self.app.post('/delete/board/1',
                           data=dict(confirm=True),
                           follow_redirects=True)
        self.assertIn(b'Board Deleted', rv.data)

    def test_add_invalid_board(self):
        self.register()
        self.login('un', 'P&ssw0rd')
        """no name"""
        rv = self.app.post('/add-board',
                           data=dict(name="", venuesize="Small", eventdate="2020-09-20"),
                           follow_redirects=True)
        self.assertIn(b'Venue Size', rv.data)
        """Too long name"""
        rv = self.app.post('/add-board',
                           data=dict(name="TestBoardTestBoardTestBoard1234", venuesize="Small", eventdate="2020-09-20"),
                           follow_redirects=True)
        self.assertIn(b'Venue Size', rv.data)

    def test_delete_invalid_board(self):
        """board does not exist"""
        self.newboard()
        rv = self.app.post('/delete/board/22',
                           data=dict(confirm=True),
                           follow_redirects=True)
        self.assertIn(b'Board does not exist', rv.data)
        """someone else's board"""
        self.newboard()
        self.logout()
        self.register(username='un1', email='email@test.com')
        self.login('un1', 'P&ssw0rd')
        rv = self.app.post('/delete/board/1',
                           data=dict(confirm=True),
                           follow_redirects=True)
        self.assertIn(b'This is not your board!', rv.data)

    def test_view_invalid_board(self):
        """Tests trying to view a board which belongs to another user"""
        self.newboard()
        self.logout()
        self.register('un1', 'email@test.com')
        self.login('un1', 'P&ssw0rd')
        rv = self.app.get('/1', follow_redirects=True)
        self.assertIn(b'This is not your board', rv.data)


if __name__ == '__main__':
    unittest.main()
