import os


def test_dashboard_exists():
    assert os.path.exists("dashboard/app.py")


def test_pages_exist():
    assert len([f for f in os.listdir("dashboard/pages") if f.endswith(".py")]) == 4


def test_model_saved():
    assert os.path.exists("models/prophet_model.json")


def test_requirements():
    assert os.path.exists("requirements.txt")
