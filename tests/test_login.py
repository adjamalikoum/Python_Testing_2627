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


def test_logout_clears_session_and_blocks_protected_page(client):
    with client.session_transaction() as sess:
        sess['email'] = 'john@simplylift.co'

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'] in ('/', 'http://localhost/')

    with client.session_transaction() as sess:
        assert 'email' not in sess

    # Accessing protected page without session must be blocked
    get_summary = client.get('/showSummary')
    assert get_summary.status_code == 302
    assert get_summary.headers['Location'] in ('/', 'http://localhost/')


def test_competitions_separated_into_upcoming_and_past(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b"Upcoming Competitions" in response.data
    assert b"Past Competitions" in response.data
    assert b"/book/Future%20Competition/Simply%20Lift" in response.data or b"/book/Future Competition/Simply Lift" in response.data
    assert b"/book/Spring%20Festival/Simply%20Lift" not in response.data and b"/book/Spring Festival/Simply Lift" not in response.data
