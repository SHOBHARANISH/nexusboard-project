def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_post_invalid(client):
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'incorrect'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data or b"Login" in response.data
