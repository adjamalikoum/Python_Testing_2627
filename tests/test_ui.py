def test_static_css_is_served_and_linked(client):
    css_response = client.get('/static/css/style.css')
    assert css_response.status_code == 200
    assert b"body" in css_response.data

    home_response = client.get('/')
    assert home_response.status_code == 200
    assert b'rel="stylesheet"' in home_response.data
    assert b'style.css' in home_response.data

    points_response = client.get('/points')
    assert points_response.status_code == 200
    assert b'rel="stylesheet"' in points_response.data
    assert b'style.css' in points_response.data
