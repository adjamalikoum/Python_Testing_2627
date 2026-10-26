import copy
import os
import sys
import pytest

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import server  # noqa: E402


@pytest.fixture
def mock_clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]


@pytest.fixture
def mock_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Future Competition",
            "date": "2028-10-22 13:30:00",
            "numberOfPlaces": "20"
        }
    ]


@pytest.fixture
def client(monkeypatch, mock_clubs, mock_competitions):
    server.app.config["TESTING"] = True
    server.app.config["SECRET_KEY"] = "test_secret_key"
    clubs_data = copy.deepcopy(mock_clubs)
    comps_data = copy.deepcopy(mock_competitions)
    monkeypatch.setattr(server, "clubs", clubs_data)
    monkeypatch.setattr(server, "competitions", comps_data)
    with server.app.test_client() as client:
        yield client
