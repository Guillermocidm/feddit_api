import pytest
import requests
BASE_URL = "http://localhost:5000/subfeddit/comments/"


def test_get_comments():
    params = {
        'name' : 'Dummy Topic 2',
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    assert response.status_code == 200    
    assert len(data) > 0
    assert list(data[0].keys()) == ['category', 'id', 'score', 'text']
    for d in data:
        assert isinstance(d['score'], float)
        assert d['score'] <= 1.0 and d['score'] >= -1.0
        if d['score'] >= 0.0:
            assert d['category'] == 'positive'
        else:
            assert d['category'] == 'negative'


def test_subfeddit_not_found():
    params = {
        'name': 'AAAA',
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 404
    assert response.json().get('error') == f"{params['name']} subfeddit not found"


def test_subfeddit_name_required():
    params = {
        'sort_by_polarity': 'true',
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 400
    assert response.json().get('error')  == "Subfeddit name is required"
