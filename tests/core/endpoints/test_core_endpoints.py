from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase


class IndexEndpointTests(APITestCase):
    def test_index_returns_200(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_index_returns_all_expected_fields(self):
        response = self.client.get("/api/v1/")
        expected_keys = {
            "name",
            "version",
            "description",
            "environment",
            "redoc_url",
            "health_url",
            "api_version",
        }
        self.assertEqual(set(response.data.keys()), expected_keys)

    def test_index_uses_project_metadata_from_settings(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(response.data["name"], settings.PROJECT_NAME)
        self.assertEqual(response.data["version"], settings.PROJECT_VERSION)
        self.assertEqual(response.data["description"], settings.PROJECT_DESCRIPTION)
        self.assertEqual(response.data["environment"], settings.ENVIRONMENT)

    def test_index_api_version_is_uppercase(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(response.data["api_version"], "V1")

    def test_index_method_not_allowed(self):
        response = self.client.post("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class HealthEndpointTests(APITestCase):
    def test_health_returns_200(self):
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_status_is_ok(self):
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.data["status"], "ok")

    def test_health_timestamp_is_iso_format(self):
        from django.utils.dateparse import parse_datetime

        response = self.client.get("/api/v1/health/")
        self.assertIsNotNone(parse_datetime(response.data["timestamp"]))

    def test_health_uptime_seconds_is_non_negative(self):
        response = self.client.get("/api/v1/health/")
        self.assertGreaterEqual(response.data["uptime_seconds"], 0)

    def test_health_method_not_allowed(self):
        response = self.client.delete("/api/v1/health/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SchemaEndpointTests(APITestCase):
    def test_schema_returns_200(self):
        response = self.client.get("/api/v1/schema/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_ui_returns_200(self):
        response = self.client.get("/api/v1/docs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_returns_200(self):
        response = self.client.get("/api/v1/redoc/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
