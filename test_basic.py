def test_home_page(client):
    """Check if the homepage loads correctly."""
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"NotifyNet" in response.data
