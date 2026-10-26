import pytest
import server


def test_points_deducted_after_booking(client):
    club_name = "Simply Lift"
    initial_points = int([c for c in server.clubs if c["name"] == club_name][0]["points"])
    places_to_book = 2

    response = client.post(
        "/purchasePlaces",
        data={
            "club": club_name,
            "competition": "Future Competition",
            "places": str(places_to_book),
        },
    )

    assert response.status_code == 200
    updated_club = [c for c in server.clubs if c["name"] == club_name][0]
    assert int(updated_club["points"]) == initial_points - places_to_book
    assert f"Points available: {initial_points - places_to_book}".encode() in response.data


def test_cannot_book_more_places_than_available(client):
    club_name = "Simply Lift"
    comp_name = "Future Competition"
    initial_comp_places = int([c for c in server.competitions if c["name"] == comp_name][0]["numberOfPlaces"])
    initial_club_points = int([c for c in server.clubs if c["name"] == club_name][0]["points"])

    places_to_book = initial_comp_places + 5
    response = client.post(
        "/purchasePlaces",
        data={
            "club": club_name,
            "competition": comp_name,
            "places": str(places_to_book),
        },
    )

    comp = [c for c in server.competitions if c["name"] == comp_name][0]
    club = [c for c in server.clubs if c["name"] == club_name][0]
    assert int(comp["numberOfPlaces"]) == initial_comp_places
    assert int(club["points"]) == initial_club_points
    assert b"Great-booking complete!" not in response.data


def test_cannot_book_more_than_12_places(client):
    club_name = "Simply Lift"
    comp_name = "Future Competition"
    initial_comp_places = int([c for c in server.competitions if c["name"] == comp_name][0]["numberOfPlaces"])
    initial_club_points = int([c for c in server.clubs if c["name"] == club_name][0]["points"])

    places_to_book = 13
    response = client.post(
        "/purchasePlaces",
        data={
            "club": club_name,
            "competition": comp_name,
            "places": str(places_to_book),
        },
    )

    comp = [c for c in server.competitions if c["name"] == comp_name][0]
    club = [c for c in server.clubs if c["name"] == club_name][0]
    assert int(comp["numberOfPlaces"]) == initial_comp_places
    assert int(club["points"]) == initial_club_points
    assert b"Great-booking complete!" not in response.data
    assert b"12" in response.data


def test_cannot_book_past_competition(client):
    club_name = "Simply Lift"
    comp_name = "Spring Festival"  # Date: 2020-03-27 10:00:00 (past)
    initial_comp_places = int([c for c in server.competitions if c["name"] == comp_name][0]["numberOfPlaces"])
    initial_club_points = int([c for c in server.clubs if c["name"] == club_name][0]["points"])

    response = client.post(
        "/purchasePlaces",
        data={
            "club": club_name,
            "competition": comp_name,
            "places": "1",
        },
    )

    comp = [c for c in server.competitions if c["name"] == comp_name][0]
    club = [c for c in server.clubs if c["name"] == club_name][0]
    assert int(comp["numberOfPlaces"]) == initial_comp_places
    assert int(club["points"]) == initial_club_points
    assert b"Great-booking complete!" not in response.data


@pytest.mark.parametrize("invalid_places", ["-2", "0", "abc", ""])
def test_cannot_book_with_invalid_places(client, invalid_places):
    club_name = "Simply Lift"
    comp_name = "Future Competition"
    initial_comp_places = int([c for c in server.competitions if c["name"] == comp_name][0]["numberOfPlaces"])
    initial_club_points = int([c for c in server.clubs if c["name"] == club_name][0]["points"])

    response = client.post(
        "/purchasePlaces",
        data={
            "club": club_name,
            "competition": comp_name,
            "places": invalid_places,
        },
    )

    comp = [c for c in server.competitions if c["name"] == comp_name][0]
    club = [c for c in server.clubs if c["name"] == club_name][0]
    assert int(comp["numberOfPlaces"]) == initial_comp_places
    assert int(club["points"]) == initial_club_points
    assert b"Great-booking complete!" not in response.data


def test_book_with_unknown_club_or_competition_does_not_crash(client):
    response_unknown_club = client.get("/book/Future Competition/Unknown Club")
    assert response_unknown_club.status_code in (200, 302)

    response_unknown_comp = client.get("/book/Unknown Competition/Simply Lift")
    assert response_unknown_comp.status_code in (200, 302)


def test_purchase_places_applies_prg(client):
    client.post("/showSummary", data={"email": "john@simplylift.co"})

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Future Competition",
            "places": "1",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"] in ("/showSummary", "http://localhost/showSummary")
