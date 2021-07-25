from main import app, conn
import models
import unittest
from flask_testing import TestCase


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertIn(b'Please login', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)
        #self.assertIn(b'The CSRF token is missing', response.data)


        # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

        # Ensure that logout page requires user login
    def test_logout_route_requires_logout(self):
        tester = app.test_client()
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    def test_main_page(self):
        with self.client:
            self.client.post('/register', data=dict(username="xyz", password="xyz"), 
                follow_redirects=True)
            self.client.post('/login', data=dict(username="xyz", password="xyz"), 
                follow_redirects=True)
            response = self.client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome', response.data)

    def test_request_page(self):
        with self.client:
            self.client.post('/login', data=dict(username="xyz", password="xyz"), 
                follow_redirects=True)
            response = self.client.get('/requests', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Here are the requests', response.data)
            
    def test_proposal_page(self):
        with self.client:
            self.client.post('/login', data=dict(username="xyz", password="xyz"), 
                follow_redirects=True)
            response = self.client.get('/proposals', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'No proposals', response.data)

    def test_request_insert(self):
        with self.client:
            self.client.post('/login', data=dict(username="xyz", password="xyz"),
                follow_redirects=True)
            self.client.post('/', data=dict(location="pakistan", meal_type="biryani", 
                time = "0:00", name="xyz")
                )
            welcome_response = self.client.get('/', follow_redirects=True)
            self.assertEqual(welcome_response.status_code, 200)
            request_response = self.client.get('/requests', follow_redirects=True)
            self.assertEqual(request_response.status_code, 200)
            self.assertIn(b'&#39;biryani&#39;', request_response.data)


    def test_proposal_insert(self):
        with self.client:
            self.client.post('/login', data=dict(username="xyz", password="xyz"),
                follow_redirects=True)
            self.client.post('/', data=dict(location="pakistan", meal_type="biryani", 
                time = "0:00", name="xyz")
                )

            cur = conn.cursor()
            conn.set_session(autocommit=True)
            cur.execute('''SELECT id FROM requests WHERE username=(%s)''', ('xyz',))
            request_id = cur.fetchone()
            cur.execute('''INSERT INTO proposals (request_id, user_to, user_from)
                VALUES (%s, %s, %s)''', (request_id, 'xyz', 'xyz'))
            cur.execute('''SELECT * FROM proposals WHERE request_id = (%s)''', (request_id,))
            row = cur.fetchone()
            print(row)
            self.client.post('/login', data=dict(username="xyz", password="xyz"), 
                follow_redirects=True)
            response = self.client.get('/proposals', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'biryani', response.data)
            cur.execute('''DELETE FROM proposals where user_to=(%s)''', ('xyz', ))
            cur.execute('''DELETE FROM requests where location=(%s)''', ('pakistan', ))
            



if __name__ == '__main__':
    cur = conn.cursor()
    conn.set_session(autocommit=True)

    #creating a role for role-based policy
    try:
            cur.execute('''CREATE ROLE readwrite''')
    except:
            print('Role already created')



    cur.execute('''GRANT CONNECT ON DATABASE postgres TO readwrite''')
    cur.execute('''GRANT SELECT, INSERT, UPDATE ON TABLE users TO readwrite''')
    cur.execute('''GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE requests TO readwrite''')
    cur.execute('''GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE proposals TO readwrite''')
    cur.execute('''GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO readwrite''')
    cur.execute('''GRANT USAGE ON SCHEMA public TO readwrite''')

    #assigning the role to the user called developer4 who will work on the main application
    try:
            cur.execute("CREATE USER developer WITH PASSWORD 'dev_pswd'")
    except:
            print('User already created')

    cur.execute('''GRANT readwrite TO developer''')

    unittest.main()
