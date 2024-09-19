import pytest
import json
import requests
from app import filter_comments_by_date, sort_comments_by_polarity
BASE_URL = "http://localhost:5000/subfeddit/comments/"

@pytest.fixture
def mock_get_comments():
    comments = [
        {'id': 1, 'text': 'This is awesome!', 'created_at': 1726704000, 'score': 1.0}, # 2024-09-19
        {'id': 2, 'text': 'This is bad...', 'created_at': 1726963200,  'score': -1.0}, #2024-09-22
        {'id': 3, 'text': 'Neutral comment.', 'created_at': 1726617600, 'score': 0.0} #2024-09-18
    ]
    return comments

# def test_get_comments():
#     params = {
#         'name' : 'Dummy Topic 2',
#     }
#     response = requests.get(BASE_URL, params=params)
#     data = response.json()

#     assert response.status_code == 200    
#     assert len(data) > 0
#     assert list(data[0].keys()) == ['category', 'id', 'score', 'text']
#     for d in data:
#         assert isinstance(d['score'], float)
#         assert d['score'] <= 1.0 and d['score'] >= -1.0
#         if d['score'] >= 0.0:
#             assert d['category'] == 'positive'
#         else:
#             assert d['category'] == 'negative'

def test_sort_by_polarity(mock_get_comments):
    sorted_comments = sort_comments_by_polarity(mock_get_comments)

    assert sorted_comments[0]['score'] == 1.0
    assert sorted_comments[1]['score'] == 0.0
    assert sorted_comments[2]['score'] == -1,0

def test_filter_by_date(mock_get_comments):
    filtered_comments = filter_comments_by_date(mock_get_comments, "2024-09-20", "2024-09-23")

    assert len(filtered_comments) == 1
    assert filtered_comments[0]['text'] == 'This is bad...'

# def test_subfeddit_not_found():
#     params = {
#         'name': 'AAAA',
#     }
#     response = requests.get(BASE_URL, params=params)

#     assert response.status_code == 404
#     assert response.json().get('error') == f"{params['name']} subfeddit not found"


def test_subfeddit_name_required():
    params = {
        'sort_by_polarity': 'true',
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 400
    assert response.json().get('error')  == "Subfeddit name is required"
