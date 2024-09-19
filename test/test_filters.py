import pytest
from app import filter_comments_by_date, sort_comments_by_polarity

@pytest.fixture
def mock_get_comments():
    comments = [
        {'id': 1, 'text': 'This is awesome!', 'created_at': 1726704000, 'score': 1.0}, # 2024-09-19
        {'id': 2, 'text': 'This is bad...', 'created_at': 1726963200,  'score': -1.0}, #2024-09-22
        {'id': 3, 'text': 'Neutral comment.', 'created_at': 1726617600, 'score': 0.0} #2024-09-18
    ]
    return comments


def test_sort_by_polarity(mock_get_comments):
    sorted_comments = sort_comments_by_polarity(mock_get_comments)

    assert sorted_comments[0]['score'] == 1.0
    assert sorted_comments[1]['score'] == 0.0
    assert sorted_comments[2]['score'] == -1,0


def test_filter_by_date(mock_get_comments):
    filtered_comments = filter_comments_by_date(mock_get_comments, "2024-09-20", "2024-09-23")

    assert len(filtered_comments) == 1
    assert filtered_comments[0]['text'] == 'This is bad...'