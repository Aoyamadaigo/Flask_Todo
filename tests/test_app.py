import unittest
from flask_testing import TestCase
from app import app,db,Task

class MyTest(TestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_task(self):
        response = self.client.get('/add_task')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
        