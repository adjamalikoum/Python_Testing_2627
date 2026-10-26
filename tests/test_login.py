from flask import session


def test_unknown_email_redirects_with_flash(client):
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    assert response.status_code == 302
    assert response.headers['Location'] in ('/', 'http://localhost/')
    flashes = session.get('_flashes', [])
    assert len(flashes) > 0
    assert 'email' in flashes[0][1].lower()
