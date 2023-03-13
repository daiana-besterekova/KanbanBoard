import pytest 
import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db
from flask import session
from flaskr.db import get_db

'''
Adapted from https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/
'''

# Opening data.sql and converting it into binary code
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

# crunning an app with temporary database 
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

# create a test client for the app 
@pytest.fixture
def client(app):
    return app.test_client()

# create CLI for the app 
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# testing functionaility of authorization 
class authorization(object):
    def __init__(self, client):
        self._client = client

    # send a POST request to the '/auth/login'
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    # send GET request to the '/auth/logout'
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'b', 'password': 'b'}
    )
    # test if registering successfully leads to login page
    assert '/auth/login' == response.headers['Location']

    # test if data is stored in the database
    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'b'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', 'password', b'Username is required.'),
    ('username', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))

# test edge case inputs and check the error message 
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

# test if the app is configured 
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

 
# test get_db function in app.py 
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    # test if login works
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    #check if logout works 
    def logout(self):
        return self._client.get('/auth/logout')

# check if successful login leads to index page 
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == '/'

# test login functionality and edge cases 
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

# test if logout works: if user logged out, they must not be in session 
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

# test if such elements exist on the page 
def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data

# test if create function works 
def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'CS111', 'body': 'Finish my assignment', 'status': 'In Process'})

    # test if the query is in the database
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2

