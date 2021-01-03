import unittest
import os
from peewee import *
import time

from models import User, Board, Idea, Idea_Tag, Tag
from tests.test_phase3idea import IdeaHelperTestCase

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect(reuse_if_open=True)
TEST_DB.drop_tables([User, Board, Idea, Idea_Tag, Tag])
TEST_DB.create_tables([User, Board, Idea, Idea_Tag, Tag], safe=True)


class PagesTestCase(IdeaHelperTestCase):
    def test_get_print(self):
        self.registerandlogin()
        rv = self.app.get('/1/print', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_get_public(self):
        # will not display public page but should still redirect to a valid page
        self.registerandlogin()
        rv = self.app.get('/public/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_get_tutorial(self):
        self.registerandlogin()
        rv = self.app.get('/tutorial', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_get_faq(self):
        self.registerandlogin()
        rv = self.app.get('/faq', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_get_suggestions(self):
        self.registerandlogin()
        rv = self.app.get('/1/suggestions', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)


class PublicPageTestCase(IdeaHelperTestCase):
    def test_page_not_public(self):
        """Tests trying to publicly view a board which is private"""
        self.registerandlogin()
        rv = self.app.get('/public/1', follow_redirects=True)
        self.assertIn(b'This board is not set to public readonly', rv.data)

    def test_page_public(self):
        """Tests setting a board to public and then viewing it"""
        self.registerandlogin()
        self.app.post('/updatetoggle/1', data=dict(publicreadonly=True))
        rv = self.app.get('/public/1')
        self.assertIn(b'Project date:', rv.data)


if __name__ == 'app':
    unittest.main()
