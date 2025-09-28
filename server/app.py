#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Clear session route
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# List all articles
@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    result = []
    for article in articles:
        result.append({
            "id": article.id,
            "title": article.title,
            "content": article.content
        })
    return jsonify(result), 200

# Show single article with session-based paywall
@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views if not set
    session['page_views'] = session.get('page_views', 0)
    session['page_views'] += 1

    # Paywall check
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    # Fetch article or 404
    article = Article.query.get_or_404(id)

    # Return article as JSON
    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content
    }), 200

if __name__ == '__main__':
    app.run(port=5555)
