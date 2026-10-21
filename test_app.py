
import app as studyflow_app


def setup_test_db(tmp_path):
    studyflow_app.DB_PATH = str(tmp_path / "test_studyflow.db")
    studyflow_app.init_db()


def test_homepage_loads(tmp_path):
    setup_test_db(tmp_path)
    client = studyflow_app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"StudyFlow" in response.data


def test_health_endpoint(tmp_path):
    setup_test_db(tmp_path)
    client = studyflow_app.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_add_task(tmp_path):
    setup_test_db(tmp_path)
    client = studyflow_app.app.test_client()

    response = client.post(
        "/tasks/add",
        data={
            "title": "Complete Python assignment",
            "subject": "Python",
            "due_date": "2026-10-25",
            "priority": "High",
        },
    )

    assert response.status_code == 302

    tasks = client.get("/api/tasks").json
    assert any(
        task["title"] == "Complete Python assignment"
        for task in tasks
    )
