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
