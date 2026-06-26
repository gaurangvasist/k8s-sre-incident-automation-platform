from fastapi.testclient import TestClient

from sre_ops_health_api.main import app


client = TestClient(app)


def test_health_returns_healthy_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready_returns_ready_by_default() -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_version_returns_app_metadata() -> None:
    response = client.get("/api/v1/version")

    assert response.status_code == 200
    body = response.json()
    assert body["app"] == "sre-ops-health-api"
    assert body["environment"] == "local"


def test_checks_returns_operations_checks() -> None:
    response = client.get("/api/v1/checks")

    assert response.status_code == 200
    body = response.json()
    check_names = {check["name"] for check in body["checks"]}
    assert "linux-patching" in check_names
    assert "backup-status" in check_names
    assert "certificate-expiry" in check_names


def test_unknown_check_returns_404() -> None:
    response = client.get("/api/v1/checks/not-a-real-check")

    assert response.status_code == 404
