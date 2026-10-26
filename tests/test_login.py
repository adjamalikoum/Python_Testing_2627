from flask import session
import server


def test_unknown_email_redirects_with_flash(client):
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    assert response.status_code == 302
    assert response.headers['Location'] in ('/', 'http://localhost/')
    flashes = session.get('_flashes', [])
    assert len(flashes) > 0
    assert 'email' in flashes[0][1].lower()


def test_flash_messages_displayed_on_index(client):
    response = client.post('/showSummary', data={'email': 'unknown@example.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, that email was not found." in response.data


def test_load_json_files_independent_of_cwd(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    assert len(clubs) > 0
    assert len(competitions) > 0
