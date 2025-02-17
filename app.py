from flask import Flask, jsonify, request, render_template
import sqlite3
import requests
import re

app = Flask(__name__)

# Fetch YouTube title dynamically
def get_youtube_title(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            match = re.search(r"<title>(.*?) - YouTube</title>", response.text)
            if match:
                return match.group(1).strip()
        return "Unknown Title"
    except:
        return "Failed to Fetch Title"

# Fetch videos from SQLite
def get_videos_from_db(page, per_page=10):
    conn = sqlite3.connect("data/youtube_history.db")
    cursor = conn.cursor()

    total_videos = cursor.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
    start = (page - 1) * per_page

    cursor.execute("SELECT url, views FROM videos ORDER BY views DESC LIMIT ? OFFSET ?", (per_page, start))
    videos = [{"url": row[0], "views": row[1]} for row in cursor.fetchall()]

    # Fetch titles dynamically
    for video in videos:
        video['title'] = get_youtube_title(video['url'])
    
    conn.close()
    return videos, (total_videos // per_page) + (1 if total_videos % per_page else 0)

@app.route("/api/videos")
def get_videos():
    page = int(request.args.get("page", 1))
    videos, total_pages = get_videos_from_db(page)
    
    return jsonify({
        "videos": videos,
        "total_pages": total_pages
    })

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
