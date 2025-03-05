import os

# Application Settings
WINDOW_TITLE = "YouTube History Recap"
WINDOW_SIZE = "1920x1080"  # Full HD resolution
WINDOW_RESIZABLE = False

# Font Configuration
FONT_FAMILY = "Comfortaa"  # Modern, clean font with excellent readability
FONT_WEIGHTS = {
    "normal": "normal",
    "bold": "bold"
}

# UI Configuration
HEADER_FONT_SIZE = 34
HEADER_PADDING = (10, 10)
BUTTON_FONT_SIZE = 15
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 35
BUTTON_CORNER_RADIUS = 8

# Button Colors
BLUE_BUTTON = {
    "fg_color": ("#2196F3", "#1976D2"),
    "hover_color": ("#1976D2", "#2196F3"),
    "border_color": ("#2196F3", "#1976D2"),
    "border_width": 2
}

RED_BUTTON = {
    "fg_color": ("#B71C1C", "#7F0000"),
    "hover_color": ("#7F0000", "#B71C1C"),
    "border_color": ("#B71C1C", "#7F0000"),
    "border_width": 2
}

# Video Entry Configuration
THUMBNAIL_SIZE = (120, 68)
THUMBNAIL_CORNER_RADIUS = 8
RANK_FONT_SIZE = 26
TITLE_FONT_SIZE = 18
COUNT_FONT_SIZE = 16

# Pagination Configuration
VIDEOS_PER_PAGE = 10
PAGINATION_BUTTON_SIZE = 50
PAGINATION_FONT_SIZE = 26
PAGINATION_ENTRY_SIZE = (70, 50)
PAGINATION_ENTRY_FONT_SIZE = 18

# Loading Screen Configuration
LOADING_FONT_SIZE = 24
LOADING_BAR_WIDTH = 300
LOADING_BAR_HEIGHT = 10
LOADING_ANIMATION_DELAY = 500  # milliseconds

# Cache Configuration
CACHE_FILENAME = "youtube_history_cache.pkl"

# Threading Configuration
MAX_THUMBNAIL_WORKERS = 10
THUMBNAIL_TIMEOUT = 5  # seconds

# Debug Configuration
DEBUG = True

# YouTube API Configuration
YOUTUBE_THUMBNAIL_URLS = {
    "maxresdefault": "https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
    "hqdefault": "https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
    "default": "https://img.youtube.com/vi/{video_id}/default.jpg"
}

# Video ID Patterns
VIDEO_ID_PATTERNS = [
    r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
    r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
    r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
] 