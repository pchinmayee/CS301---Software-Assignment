import pytest
import json
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('mysql.connector.connect')
def test_get_artists(mock_connect, client):
    mock_cursor = MagicMock()
    mock_rows = [(1, 'John Doe', 'A talented painter', 'johndoe@example.com'), 
                 (2, 'Jane Doe', 'An up-and-coming musician', 'janedoe@example.com')]
    mock_cursor.fetchall.return_value = mock_rows
    mock_connect.return_value.cursor.return_value = mock_cursor

    response = client.get('/artists')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    artists = json.loads(response.data)
    assert isinstance(artists, list)
    assert len(artists) == len(mock_rows)

@patch('mysql.connector.connect')
def test_create_artist(mock_connect, client):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor

    artist = {'name': 'John Doe', 'email': 'johndoe@example.com', 'description': 'A talented painter'}
    response = client.post('/artists', data=artist)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    message = json.loads(response.data)
    assert message['message'] == 'Artist added successfully'

    mock_cursor.execute.assert_called_once_with(
        'INSERT INTO artists (id, name, description, email) VALUES (%s, %s, %s, %s)',
        (pytest.any(), 'John Doe', 'A talented painter', 'johndoe@example.com')
    )

