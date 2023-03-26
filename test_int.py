from app import app
import unittest
import json

class TestArtists(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_artists(self):
        response = self.app.get('/artists')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        artists = json.loads(response.data)
        self.assertTrue(isinstance(artists, list))

    def test_create_artist(self):
        artist = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'description': 'A talented painter'
        }
        response = self.app.post('/artists', data=artist)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        message = json.loads(response.data)
        self.assertEqual(message['message'], 'Artist added successfully')

if __name__ == '__main__':
    unittest.main()
