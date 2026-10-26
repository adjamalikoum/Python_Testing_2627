import server


def test_points_deducted_after_booking(client):
    club_name = "Simply Lift"
    initial_points = int([c for c in server.clubs if c["name"] == club_name][0]["points"])
    places_to_book = 2

    response = client.post(
        "/purchasePlaces",
        data={
            "club": club_name,
            "competition": "Spring Festival",
            "places": str(places_to_book),
        },
    )

    assert response.status_code == 200
    updated_club = [c for c in server.clubs if c["name"] == club_name][0]
    assert int(updated_club["points"]) == initial_points - places_to_book
    assert f"Points available: {initial_points - places_to_book}".encode() in response.data


def test_cannot_book_more_places_than_available(client):
    club_name = "Simply Lift"
    comp_name = "Spring Festival"
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
    comp_name = "Spring Festival"
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
