def test_points_display_page_is_public_and_lists_clubs(client):
    response = client.get("/points")
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data
    assert b'href="/"' in response.data or b"href='/'" in response.data
