from lxml import etree
import sqlite3
from collections import Counter

# Input file (Google Takeout HTML)
input_file = "data/takeout.html"
db_file = "data/youtube_history.db"

# Create or connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        url TEXT PRIMARY KEY,
        views INTEGER
    )
""")
conn.commit()

# Extract YouTube links
def extract_links(file):
    links = []
    context = etree.iterparse(file, html=True, events=("start", "end"))

    for event, elem in context:
        if event == "start" and elem.tag == "div" and "content-cell" in elem.get("class", ""):
            link = elem.find(".//a")
            if link is not None and "youtube.com/watch" in link.get("href", ""):
                links.append(link.get("href"))
            elem.clear()  # Free memory

    return links

# Count views per video
def count_views(links):
    counter = Counter(links)
    return {link: count for link, count in counter.items() if count > 1}  # Remove single-view videos

# Process the HTML file
links = extract_links(input_file)
views = count_views(links)

# Insert data into SQLite
for link, count in views.items():
    cursor.execute("INSERT OR REPLACE INTO videos (url, views) VALUES (?, ?)", 
                   (link, count))

conn.commit()
conn.close()

print(f"Processing complete. Saved {len(views)} videos to SQLite database.")
