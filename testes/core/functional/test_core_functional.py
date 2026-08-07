import time
from datetime import datetime

from rest_framework.test import APITestCase

from core import uptime


class IndexFunctionalTests(APITestCase):
    def test_health_url_points_to_live_health_endpoint(self):
        index_response = self.client.get("/api/v1/")
        health_url = index_response.data["health_url"]
        health_response = self.client.get(health_url)
        self.assertEqual(health_response.status_code, 200)
        self.assertEqual(health_response.data["status"], "ok")

    def test_redoc_url_points_to_live_redoc_endpoint(self):
        index_response = self.client.get("/api/v1/")
        redoc_url = index_response.data["redoc_url"]
        redoc_response = self.client.get(redoc_url)
        self.assertEqual(redoc_response.status_code, 200)

    def test_environment_matches_test_settings(self):
        from django.conf import settings

        index_response = self.client.get("/api/v1/")
        self.assertEqual(index_response.data["environment"], settings.ENVIRONMENT)


class HealthFunctionalTests(APITestCase):
    def test_uptime_increases_between_requests(self):
        first = self.client.get("/api/v1/health/").data["uptime_seconds"]
        time.sleep(1.1)
        second = self.client.get("/api/v1/health/").data["uptime_seconds"]
        self.assertGreater(second, first)

    def test_uptime_is_computed_from_process_start(self):
        now = datetime.now(tz=uptime.START_TIME.tzinfo)
        expected_uptime = (now - uptime.START_TIME).total_seconds()
        response = self.client.get("/api/v1/health/")
        self.assertAlmostEqual(
            response.data["uptime_seconds"], expected_uptime, delta=5
        )

    def test_timestamp_is_aware_datetime(self):
        from django.utils.dateparse import parse_datetime

        response = self.client.get("/api/v1/health/")
        parsed = parse_datetime(response.data["timestamp"])
        self.assertIsNotNone(parsed)
        self.assertTrue(parsed.tzinfo is not None and parsed.utcoffset() is not None)
