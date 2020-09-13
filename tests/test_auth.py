import unittest
import os
from peewee import *

import app
from models import User, Board

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect(reuse_if_open=True)
TEST_DB.create_tables([User], safe=True)


class AppTestCase(unittest.TestCase):
    """class providing test setUp for future tests to inherit"""
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        TEST_DB.drop_tables([User, Board])
        TEST_DB.create_tables([User, Board])
        self.app = app.app.test_client()


class LoadPagesTestCase(AppTestCase):
    def test_index_page(self):
        rv = self.app.get('/', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_login_page(self):
        rv = self.app.get('/login', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_register_page(self):
        rv = self.app.get('/register', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)


class UserModelTestCase(AppTestCase):
    """helper methods to facilitate user tests"""
    def register(self, username='un', email='06gwaller@brightoncollege.net', password='P&ssw0rd', usertype='Designer'):
        return self.app.post(
            '/register',
            data=dict(username=username, password=password, password2=password, email=email, usertype=usertype),
            follow_redirects=True
        )

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_valid_user_registration(self):
        """tests that a user with valid details can register"""
        rv = self.register('User1', 'email8@testing.com', 'Ryehouse80!', usertype='Designer')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Registration successful', rv.data)

    def test_invalid_user_registration(self):
        """tests registering with invalid credentials"""
        """test data"""
        usernames = ['', 'qla b', 'QL&B', 'qlabqlabqlabqlabqlab1']
        emails = ['', '@gmail.com', 'user@testserver.com', 'user']
        passwords = ['', 'Ryehous|', 'RYEH0US|', 'ryeh0us|', 'Ryeh0use', 'f1&sk', 'Ryeh0use&Metrobus1234']
        """invalid username"""
        for i in range(len(usernames)):
            TEST_DB.drop_tables([User])
            TEST_DB.create_tables([User])
            rv = self.register(username=usernames[i])
            self.assertIn(b'error', rv.data)
        """invalid email"""
        for j in range(len(emails)):
            TEST_DB.drop_tables([User])
            TEST_DB.create_tables([User])
            rv = self.register(email=emails[j])
            self.assertIn(b'error', rv.data)
        """invalid password"""
        for k in range(len(passwords)):
            TEST_DB.drop_tables([User])
            TEST_DB.create_tables([User])
            rv = self.register(password=passwords[k])
            self.assertIn(b'error', rv.data)
        """non-matching passwords"""
        rv = self.app.post(
            '/register',
            data=dict(username='George_', password='Ryeh0us|', password2='Ry3h0us|', email='email@gmail.com'),
            follow_redirects=True
        )
        self.assertIn(b'error', rv.data)
        """previously registered email"""
        self.register(username='Test111', email='george.waller@gmail.com')
        rv = self.register(username='Test112', email='george.waller@gmail.com')
        self.assertIn(b'error', rv.data)
        """previously registered username"""
        self.register(username='Test111', email='george.waller@gmail.com')
        rv = self.register(username='Test111', email='george.waller52@gmail.com')
        self.assertIn(b'error', rv.data)

    def test_valid_login(self):
        """tests logging in with valid credentials"""
        self.register('User1', 'email@testing.com', 'Ryehouse80!')
        rv = self.login('User1', 'Ryehouse80!')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome', rv.data)

    def test_invalid_login(self):
        """tests logging in with invalid credentials"""
        self.register()
        """wrong password"""
        rv = self.login('un', 'password')
        self.assertIn(b'Login', rv.data)
        """wrong username"""
        rv = self.login('uname', 'P&ssw0rd')
        self.assertIn(b'Login', rv.data)

    def test_logout(self):
        """tests logging out"""
        self.register()
        rv = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertNotIn(b'logged in', rv.data)


if __name__ == '__main__':
    unittest.main()
