"""Unit tests for the authorization module."""

from unittest import TestCase
from gateway.api_v1 import *


class TestServicesEndpoints(TestCase):
    """Test that endpoint is set from the right key:value pair."""

    def setUp(self):
        """Set it up."""
        self.app = app.test_client()

    def test_root_endpoint(self):
        """Test list of supported services."""
        response = self.app.get('/')
        data = json.loads(response.get_data().decode("utf-8"))
        assert data == {'services': ['data_importer', 'gremlin', 'jobs']}

    def test_gremlin(self):
        """Gremlin service."""
        response = self.app.get('/gremlin/test')
        assert response.status_code == 500
        assert b'gremlin-service:8182/test is not available' in response.data

    def test_data_importer(self):
        """Data importer service."""
        response = self.app.get('/data_importer/pending')
        assert response.status_code == 500
        assert b'data-model-importer:9192/pending is not available' in response.data

    def test_jobs(self):
        """Jobs service."""
        response = self.app.get('/jobs/test')
        assert response.status_code == 500
        assert b'jobs-service:34000/test is not available' in response.data
