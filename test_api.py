import unittest
from main import app
import json

class FlaskAPITest(unittest.TestCase):
    token = ""
    headers ={}
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"Flask-API Develop Login": "1.0"})
    
    def test_login(self):
        response = self.app.post("/login", 
                                 data = json.dumps({"email" : "admin@mail.com", "password":"12345"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Store token in global variable
        self.token = response.get_json()["token"]
        self.headers = { "Authorization" : "Bearer " + self.token , "Content-Type" : "application/json" }

    def test_products(self):
        # Call test_login() so that headers is give the token value
        self.test_login()
        response = self.app.get('/api/products', headers = self.headers)
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_products(self):
        self.test_login()
        response = self.app.post("/api/products", data=json.dumps({"name":"test product", "bp":100, "sp": 200}), 
                                 headers = self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(),{"name":"test product","bp":100,"sp": 200})

if __name__ == "__main__":
    unittest.main()