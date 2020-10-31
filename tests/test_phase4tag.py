import unittest
import os
from peewee import *
import time

import app
from models import User, Board, Idea, Idea_Tag, Tag
from tests.test_phase3idea import IdeaHelperTestCase

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect(reuse_if_open=True)
TEST_DB.drop_tables([User, Board, Idea, Idea_Tag, Tag])
TEST_DB.create_tables([User, Board, Idea, Idea_Tag, Tag], safe=True)


class PagesTestCase(IdeaHelperTestCase):
    def test_get_create_tag(self):
        self.registerandlogin()
        rv = self.app.get('/1/add-tag', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_get_delete_tag(self):
        self.registerandlogin()
        rv = self.app.get('/1/delete-tag', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_get_invalid_board(self):
        self.registerandlogin()
        rv = self.app.get('/3/delete-tag', follow_redirects=True)
        self.assertIn(b'error', rv.data)

    def test_post_valid_create_tag(self):
        self.registerandlogin()
        rv = self.app.post('/1/add-tag', data=dict(name='New Tag', colour='black'), follow_redirects=True)
        self.assertIn(b'Tag added', rv.data)

    def test_post_valid_delete_tag(self):
        self.registerandlogin()
        rv = self.app.post('/1/delete-tag', data=dict(selectTag='3', confirm=True), follow_redirects=True)
        self.assertIn(b'Tag Deleted', rv.data)

    def test_invalid_user_create_tag(self):
        self.registerandlogin()
        self.logout()
        self.register(username='un1', email='07gwaller@brightoncollege.net')
        self.login(username='un1', password='P&ssw0rd')
        rv = self.app.post('/1/add-tag', data=dict(name='New Tag', colour='black'), follow_redirects=True)
        self.assertIn(b'error', rv.data)

    def test_invalid_user_delete_tag(self):
        self.registerandlogin()
        self.logout()
        self.register(username='un1', email='07gwaller@brightoncollege.net')
        self.login(username='un1', password='P&ssw0rd')
        rv = self.app.post('/1/delete-tag', data=dict(selectTag='3', confirm=True), follow_redirects=True)
        self.assertIn(b'error', rv.data)


class InvalidFormsTestCase(IdeaHelperTestCase):
    def test_invalid_create_tag(self):
        self.registerandlogin()

        # name required
        rv = self.app.post('/1/add-tag', data=dict(name='', colour='black', follow_redirects=True))
        self.assertIn(b'error', rv.data)

        # max length 30
        rv = self.app.post('/1/add-tag', data=dict(name='Thisnameis31characters--toolong', colour='black',
                                                   follow_redirects=True))
        self.assertIn(b'error', rv.data)

    def test_invalid_delete_tag(self):
        self.registerandlogin()

        # no choice
        rv = self.app.post('/1/delete-tag', data=dict(selectTag='', confirm=True), follow_redirects=True)
        self.assertIn(b'error', rv.data)

        # not confirmed
        rv = self.app.post('/1/delete-tag', data=dict(selectTag='1'), follow_redirects=True)
        self.assertIn(b'error', rv.data)

        # invalid selection
        rv = self.app.post('/1/delete-tag', data=dict(selectTag='100', confirm=True), follow_redirects=True)
        self.assertIn(b'error', rv.data)


class IdeaSortingTestCase(IdeaHelperTestCase):
    """Testing the sorting queries by checking for ideas with only that tag"""
    def test_custom_query(self):
        self.registerandlogin()
        rv = self.app.get('/1?filter=1', follow_redirects=True)
        self.assertIn(b'To add a sense of control and searching I will use maglight torches held by each actor and '
                      b'used throughout the piece to convey their meaning.', rv.data)

    def test_colour_query(self):
        self.registerandlogin()
        rv = self.app.get('/1?filter=Colour', follow_redirects=True)
        self.assertIn(b'The void is a very sterile and harsh environment where no shadows should be present, '
                      b'it is where the actors have gone after death and are searching for the meaning of their '
                      b'death/fate.', rv.data)

    def test_all_query(self):
        self.registerandlogin()
        rv = self.app.get('/1?filter=All', follow_redirects=True)
        self.assertIn(b'This is a sample board based off a real project. It indicates the possibilities of what you '
                      b'can do on the platform. A key feature is the use of tags in the bar above,', rv.data)
