import unittest
from http.server import HTTPServer
from unittest.mock import patch
from urllib.request import urlopen
import threading
import json

from cisco import MaliciousURLLookup  # Import your script containing the MaliciousURLLookup class

class TestMaliciousURLLookup(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer(('localhost', 8080), MaliciousURLLookup)

        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        # Shutdown the server
        self.server.shutdown()
        self.server.server_close()

    def test_safe_url(self):
        with urlopen('http://localhost:8080/v1/urlinfo/ali213.net') as response:
            data = json.loads(response.read().decode('utf-8'))
            self.assertFalse(data['safe'])
            self.assertEqual(data['message'], 'This URL might contain adware.')

    def test_malicious_url(self):
        with urlopen('http://localhost:8080/v1/urlinfo/theteflacademy.co.uk') as response:
            data = json.loads(response.read().decode('utf-8'))
            self.assertFalse(data['safe'])
            self.assertEqual(data['message'], 'This URL is known to contain malware.')

    def test_unknown_url(self):
        with urlopen('http://localhost:8080/v1/urlinfo/unknownurl.com') as response:
            data = json.loads(response.read().decode('utf-8'))
            self.assertTrue(data['safe'])
            self.assertEqual(data['message'], 'The URL entered is not in the blacklist')

if __name__ == '__main__':
    unittest.main()