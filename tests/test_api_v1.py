"""Unit tests for the authorization module."""

import json
from unittest import TestCase
from gateway.api_v1 import app


class TestServicesEndpoints(TestCase):
    """Test that endpoint is set from the right key:value pair."""

    def setUp(self):
        """Set it up."""
        self.app = app.test_client()

    def test_root_endpoint(self):
        """Test list of supported services."""
        response = self.app.get('/')
        data = json.loads(response.get_data().decode("utf-8"))
        assert data == {'services': ['data_importer', 'gremlin', 'gremlin_ingestion', 'jobs']}

    def test_gremlin(self):
        """Gremlin service."""
        response = self.app.get('/gremlin/test')
        assert response.status_code == 500

    def test_unknown_service(self):
        """Data importer service."""
        response = self.app.get('/unknown/')
        assert response.status_code == 400
        data = json.loads(response.get_data().decode("utf-8"))
        assert 'error' in data
