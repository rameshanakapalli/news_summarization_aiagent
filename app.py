from flask import Flask, render_template, request, jsonify
from utils.news_api import fetch_news
from utils.summarization import summarize_text

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_news", methods=["POST"])
def get_news():
    topic = request.json["topic"]
    articles = fetch_news(topic)
    if articles:
        summaries = []
        for article in articles:
            summary = summarize_text(article["description"])
            summaries.append({
                "title": article["title"],
                "summary": summary,
                "url": article["url"],
            })
        return jsonify(summaries)
    else:
        return jsonify({"error": "Failed to fetch news"}), 500

if __name__ == "__main__":
    app.run(debug=True)
