import unittest
import os
from peewee import *
import time

import app
from models import User, Board, Idea
from tests.test_auth import UserModelTestCase

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect(reuse_if_open=True)
TEST_DB.drop_tables([User, Board, Idea])
TEST_DB.create_tables([User, Board, Idea], safe=True)


class IdeaHelperTestCase(UserModelTestCase):
    """Helper functions"""

    def newboard(self):
        self.register()
        self.login('un', 'P&ssw0rd')
        self.app.post('/add-board',
                      data=dict(name="TestBoard", venuesize="Small", eventdate="2020-09-20"),
                      follow_redirects=True)

    def newidea(self):
        self.newboard()
        self.app.post('/1/new-idea',
                      data=dict(name='Test Idea', content='This is a test new idea.', colour='white',
                                     fixturetype='', fixtureangle='', red='', green='', blue='', yellow=''),
                      follow_redirects=True)


class GetPagesTestCase(IdeaHelperTestCase):
    """Performs get requests on all new pages"""

    def test_view_board(self):
        self.newboard()
        rv = self.app.get('/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_add_idea(self):
        rv = self.app.get('/1/new-idea', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_view_idea(self):
        self.newidea()
        rv = self.app.get('/1/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_delete_idea(self):
        self.newboard()
        rv = self.app.get('/delete/idea/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)


class PostPagesTestCase(IdeaHelperTestCase):
    """Performs post requests on new forms"""

    def test_add_valid_idea(self):
        self.newboard()
        rv = self.app.post('/1/new-idea',
                           data=dict(name='Test Idea', content='This is a test new idea.', colour='white',
                                     fixturetype='', fixtureangle='', red='', green='', blue='', yellow=''),
                           follow_redirects=True)
        self.assertIn(b'Idea Created', rv.data)

    def test_edit_valid_idea(self):
        self.newidea()
        rv = self.app.post('/1/1',
                           data=dict(name='Test Idea', content='This is an edited idea.', colour='white',
                                     fixturetype='', fixtureangle='', red='', green='', blue='', yellow=''),
                           follow_redirects=True)
        self.assertIn(b'This is an edited idea.', rv.data)

    def test_delete_valid_idea(self):
        self.newidea()
        rv = self.app.post('/delete/idea/1',
                           data=dict(confirm=True),
                           follow_redirects=True)
        self.assertIn(b'Idea Deleted', rv.data)


class PostInvalidPagesTestCase(IdeaHelperTestCase):
    """Tests posting invalid data"""

    def test_invalid_idea_form(self):
        """test name field"""
        self.newboard()
        # no name
        rv = self.app.post('/1/new-idea',
                           data=dict(name='', content='test content'),
                           follow_redirects=True)
        self.assertIn(b'required', rv.data)
        # name over 30 characters
        rv = self.app.post('/1/new-idea',
                           data=dict(name='namenamenamenamenamenamenamenam', content='test content'),
                           follow_redirects=True)
        self.assertIn(b'Name must be max 30 characters', rv.data)

        """test content field"""
        # no content
        rv = self.app.post('/1/new-idea',
                           data=dict(name='Test Idea', content=''),
                           follow_redirects=True)
        self.assertIn(b'required', rv.data)
        # content over 1000 characters
        string = ('a' * 1001)
        rv = self.app.post('/1/new-idea',
                           data=dict(name='Test Idea', content=string),
                           follow_redirects=True)
        self.assertIn(b'Content cannot be over 1000 characters', rv.data)

    def test_new_idea_invalid_board(self):
        """Test adding new idea to invalid board"""
        self.register()
        self.login('un', 'P&ssw0rd')
        rv = self.app.post('/1/new-idea',
                           data=dict(name='Test Idea', content='This is a test new idea.'),
                           follow_redirects=True)
        self.assertIn(b'error', rv.data)

    def test_new_idea_wrong_user(self):
        """Test adding new idea to board of another user"""
        self.newboard()
        self.logout()
        self.register(username='test1', email='george.waller3@gmail.com')
        self.login('test1', 'P&ssw0rd')
        rv = self.app.post('/1/new-idea',
                           data=dict(name='Test Idea', content='This is a test new idea.'),
                           follow_redirects=True)
        self.assertIn(b'error', rv.data)

    def test_edit_idea_invalid_id(self):
        """test editing an idea with invalid ids"""
        # invalid boardid
        self.newidea()
        rv = self.app.post('/2/1',
                           data=dict(name='Test Idea', content='This is an edited idea.'),
                           follow_redirects=True)
        self.assertIn(b'error', rv.data)
        # invalid ideaid
        rv = self.app.post('/1/2',
                           data=dict(name='Test Idea', content='This is an edited idea.'),
                           follow_redirects=True)
        self.assertIn(b'error', rv.data)

    def test_edit_idea_wrong_user(self):
        """checks user owns the board"""
        self.newidea()
        self.logout()
        self.register(username='test1', email='george.waller3@gmail.com')
        self.login('test1', 'P&ssw0rd')
        rv = self.app.post('/1/1',
                           data=dict(name='Test Idea', content='This is an edited idea.'),
                           follow_redirects=True)
        self.assertIn(b'error', rv.data)

    def test_delete_idea_invalid_id(self):
        """tests trying to delete an idea that doesnt exist"""
        self.newidea()
        rv = self.app.post('/delete/idea/2',
                           data=dict(confirm=True),
                           follow_redirects=True)
        self.assertIn(b'Idea does not exist', rv.data)

    def test_delete_idea_wrong_user(self):
        """tests trying to delete an idea not belonging to the user"""
        self.newidea()
        self.logout()
        self.register(username='test1', email='george.waller3@gmail.com')
        self.login('test1', 'P&ssw0rd')
        rv = self.app.post('/delete/idea/1',
                           data=dict(confirm=True),
                           follow_redirects=True)
        self.assertIn(b'error', rv.data)

    def test_delete_idea_not_confirm(self):
        """tests trying to delete without confirming"""
        self.newidea()
        rv = self.app.post('/delete/idea/1',
                           data=dict(),
                           follow_redirects=True)
        self.assertIn(b'required', rv.data)


if __name__ == '__main__':
    unittest.main()
