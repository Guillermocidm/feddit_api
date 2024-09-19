from flask import Flask, request, jsonify
from app.models import TextBlobSentimentAnalysis
import requests
from datetime import datetime

app = Flask(__name__)

sentiment_analysis_model = TextBlobSentimentAnalysis()

def get_subfeddit_id_by_name(name):
    skip = 0
    limit = 10
    while True:
        try:
            response = requests.get(f"http://feddit:8080/api/v1/subfeddits/?skip={skip}&limit={limit}")
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"Error {error}")
            return None
        subfeddits = response.json().get("subfeddits")
        for subfeddit in subfeddits:
            if subfeddit['title'] == name:
                    return subfeddit['id']
        if len(subfeddits) < limit:
            break
        skip += limit
    return None

def get_comments_by_subfeddit_id(id, skip = 0, limit = 50):
    url = "http://feddit:8080/api/v1/comments/"
    parameters = f"?subfeddit_id={id}&skip={skip}&limit={limit}"
    try:
        response = requests.get(url+parameters)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(f"Error {error}")
        return None
    comments = response.json().get('comments')
    return comments

def filter_comments_by_date(comments, start_time=None, end_time=None):
    """Filters comments by date range."""
    filtered_comments = []
    for comment in comments:
        comment_time = datetime.fromtimestamp(comment['created_at'])
        if start_time:
            start_time_dt = datetime.strptime(start_time, '%Y-%m-%d')
            if comment_time < start_time_dt:
                continue
        if end_time:
            end_time_dt = datetime.strptime(end_time, '%Y-%m-%d')
            if comment_time > end_time_dt:
                continue
        filtered_comments.append(comment)
    return filtered_comments

def sort_comments_by_polarity(scored_comments):
    """Sorts comments by polarity score."""
    scored_comments.sort(key=lambda x: x['score'], reverse=True)
    return scored_comments
    

@app.route('/subfeddit/comments/', methods=['GET'])
def get_subfeddit_comments():
    try:
        name = request.args.get('name')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time') 
        sort_by_polarity = request.args.get('sort_by_polarity', 'false').lower() == 'true'

        if not name:
            return jsonify({"error": "Subfeddit name is required"}), 400

        subfeddit_id = get_subfeddit_id_by_name(name)
        if not subfeddit_id:
            return jsonify({"error": f"{name} subfeddit not found"}), 404

        comments = get_comments_by_subfeddit_id(subfeddit_id)
        if not comments:
            return jsonify({"error": "No comments found"}), 404

        if start_time and end_time:
            comments = filter_comments_by_date(comments, start_time, end_time)

        scored_comments = []
        for comment in comments:
            polarity_score = sentiment_analysis_model.classify(comment['text'])
            scored_comments.append({
                'id': comment['id'],
                'text': comment['text'],
                'score': polarity_score,
                'category' : "positive" if polarity_score >= 0 else "negative"
            })

        if sort_by_polarity:
            scored_comments = sort_comments_by_polarity(scored_comments)

        return jsonify(scored_comments), 200
    except Exception as e:
        return jsonify({"error" : f"Error {e}"}), 500

@app.route('/test', methods=['POST'])
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)