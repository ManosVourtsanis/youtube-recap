import customtkinter as ctk
from bs4 import BeautifulSoup
from collections import Counter
import os
from tkinter import filedialog, messagebox
from PIL import Image
import re
import traceback
import sys
import requests
import webbrowser
from io import BytesIO
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor
from settings import *

DEBUG = True

def show_error_and_exit(error_msg):
    print(error_msg)
    messagebox.showerror("Error", error_msg)
    sys.exit(1)

class LoadingScreen(ctk.CTkFrame):
    def __init__(self, parent, message="Loading...", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color="transparent")
        
        # Create semi-transparent overlay with darker background
        self.overlay = ctk.CTkFrame(self)
        self.overlay.configure(fg_color=("gray80", "gray20"))
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Create loading container
        self.loading_container = ctk.CTkFrame(self.overlay, fg_color="transparent")
        self.loading_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create loading message with larger font
        self.message = ctk.CTkLabel(
            self.loading_container,
            text=message,
            font=ctk.CTkFont(size=LOADING_FONT_SIZE, weight="bold")
        )
        self.message.pack(pady=(0, 20))
        
        # Create progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.loading_container, 
            width=LOADING_BAR_WIDTH, 
            height=LOADING_BAR_HEIGHT
        )
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        # Create loading animation (dots)
        self.dots = ""
        self.animate()
        
    def animate(self):
        self.dots = "." * ((len(self.dots) + 1) % 4)
        self.message.configure(text=f"{self.message.cget('text').split('...')[0]}{self.dots}")
        # Animate progress bar
        current = self.progress_bar.get()
        self.progress_bar.set((current + 0.1) % 1)
        self.after(LOADING_ANIMATION_DELAY, self.animate)

class ModernPagination(ctk.CTkFrame):
    def __init__(self, parent, current_page, total_pages, on_page_change, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color="transparent")
        
        # Store the callback and page info
        self.on_page_change = on_page_change
        self.total_pages = total_pages
        self.current_page = current_page
        
        # Main container for pagination
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="x", padx=10, pady=5)
        
        # Page numbers container
        self.pages_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.pages_frame.pack(expand=True)
        
        # Previous button (always visible)
        self.prev_btn = ctk.CTkButton(
            self.pages_frame,
            text="←",
            command=lambda: on_page_change(current_page - 1),
            font=ctk.CTkFont(size=PAGINATION_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY),
            width=PAGINATION_BUTTON_SIZE,
            height=PAGINATION_BUTTON_SIZE,
            corner_radius=25,
            fg_color=("gray95", "gray25"),
            hover_color=("gray90", "gray30"),
            text_color=("gray40", "gray60")
        )
        self.prev_btn.pack(side="left", padx=5)
        if current_page <= 0:
            self.prev_btn.configure(state="disabled")
        
        # Page input frame with modern styling
        self.page_frame = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        self.page_frame.pack(side="left", padx=10)
        
        # Page input with modern styling
        self.page_entry = ctk.CTkEntry(
            self.page_frame,
            width=PAGINATION_ENTRY_SIZE[0],
            height=PAGINATION_ENTRY_SIZE[1],
            font=ctk.CTkFont(size=PAGINATION_ENTRY_FONT_SIZE, family=FONT_FAMILY),
            justify="center",
            corner_radius=25,
            border_width=2,
            fg_color=("gray95", "gray25"),
            border_color=("gray90", "gray30"),
            text_color=("gray40", "gray60")
        )
        self.page_entry.pack(side="left", padx=5)
        self.page_entry.insert(0, str(current_page + 1))
        self.page_entry.bind("<Return>", lambda e: self.go_to_page())
        
        # "of X" label with modern styling
        self.page_label = ctk.CTkLabel(
            self.page_frame,
            text=f"of {total_pages}",
            font=ctk.CTkFont(size=PAGINATION_ENTRY_FONT_SIZE, family=FONT_FAMILY),
            text_color=("gray40", "gray60")
        )
        self.page_label.pack(side="left", padx=5)
        
        # Next button (always visible)
        self.next_btn = ctk.CTkButton(
            self.pages_frame,
            text="→",
            command=lambda: on_page_change(current_page + 1),
            font=ctk.CTkFont(size=PAGINATION_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY),
            width=PAGINATION_BUTTON_SIZE,
            height=PAGINATION_BUTTON_SIZE,
            corner_radius=25,
            fg_color=("gray95", "gray25"),
            hover_color=("gray90", "gray30"),
            text_color=("gray40", "gray60")
        )
        self.next_btn.pack(side="left", padx=5)
        if current_page >= total_pages - 1:
            self.next_btn.configure(state="disabled")

    def go_to_page(self):
        try:
            page = int(self.page_entry.get()) - 1
            if 0 <= page < self.total_pages:
                self.on_page_change(page)
            else:
                messagebox.showerror("Error", f"Page number must be between 1 and {self.total_pages}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid page number")

class VideoEntry(ctk.CTkFrame):
    def __init__(self, parent, title, count, video_id, rank, thumbnail, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color=("gray95", "gray15"), corner_radius=8)
        
        # Add rank number with better styling
        self.rank_label = ctk.CTkLabel(
            self,
            text=f"#{rank}",
            font=ctk.CTkFont(size=RANK_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY),
            width=60,
            text_color=("gray40", "gray60")
        )
        self.rank_label.grid(row=0, column=0, padx=(15,10), pady=15)
        
        # Create thumbnail frame with border and fixed aspect ratio
        self.thumb_frame = ctk.CTkFrame(
            self, 
            width=THUMBNAIL_SIZE[0],
            height=THUMBNAIL_SIZE[1],
            corner_radius=THUMBNAIL_CORNER_RADIUS,
            fg_color=("gray90", "gray20")
        )
        self.thumb_frame.grid(row=0, column=1, padx=(5,20), pady=15)
        self.thumb_frame.grid_propagate(False)
        
        # Load thumbnail with proper aspect ratio and make it clickable
        if thumbnail:
            self.thumb_button = ctk.CTkButton(
                self.thumb_frame,
                image=thumbnail,
                text="",
                corner_radius=THUMBNAIL_CORNER_RADIUS,
                fg_color="transparent",
                hover_color=("gray85", "gray25"),
                command=lambda: webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")
            )
            self.thumb_button.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.thumb_label = ctk.CTkLabel(
                self.thumb_frame, 
                text="No thumbnail",
                font=ctk.CTkFont(size=TITLE_FONT_SIZE, family=FONT_FAMILY),
                text_color=("gray50", "gray50")
            )
            self.thumb_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create info frame with better spacing
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=0, column=2, sticky="nsew", pady=15)
        
        # Add title as clickable link with better styling
        self.title_button = ctk.CTkButton(
            self.info_frame,
            text=title,
            command=lambda: webbrowser.open(f"https://www.youtube.com/watch?v={video_id}"),
            fg_color="transparent",
            text_color=("blue", "light blue"),
            hover_color=("gray90", "gray20"),
            anchor="w",
            font=ctk.CTkFont(size=TITLE_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY),
            height=35
        )
        self.title_button.pack(fill="x", padx=5, pady=(2,5))
        
        # Add watch count with better styling
        self.count_label = ctk.CTkLabel(
            self.info_frame,
            text=f"Watched {count} times",
            font=ctk.CTkFont(size=COUNT_FONT_SIZE, family=FONT_FAMILY),
            text_color=("gray50", "gray50"),
            anchor="w"
        )
        self.count_label.pack(fill="x", padx=5, pady=(0,2))

class YouTubeHistoryApp(ctk.CTk):
    def __init__(self):
        try:
            super().__init__()

            # Configure window with fixed size
            self.title(WINDOW_TITLE)
            self.geometry(WINDOW_SIZE)
            self.resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)
            
            # Configure grid layout
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)

            # Initialize pagination variables
            self.loading_screen = None
            self.current_page = 0
            self.videos_per_page = VIDEOS_PER_PAGE
            self.all_videos = []
            self.total_pages = 0
            
            # Cache file path
            self.cache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), CACHE_FILENAME)

            # Create header frame with buttons and navigation
            self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=HEADER_PADDING)
            self.header_frame.grid_columnconfigure(0, weight=1)
            
            # Create header with better styling
            header_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
            header_container.pack(side="left", padx=(0, 20))
            
            # Add title
            self.header = ctk.CTkLabel(
                header_container, 
                text=WINDOW_TITLE,
                font=ctk.CTkFont(size=HEADER_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY)
            )
            self.header.pack(side="left")
            
            # Create buttons frame in header
            self.buttons_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
            self.buttons_frame.pack(side="right", padx=(10, 0))
            
            # Create Load New File button
            self.new_file_btn = ctk.CTkButton(
                self.buttons_frame,
                text="Load New File",
                command=self.upload_file,
                font=ctk.CTkFont(size=BUTTON_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY),
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                corner_radius=BUTTON_CORNER_RADIUS,
                **BLUE_BUTTON
            )
            self.new_file_btn.pack(side="left", padx=5)
            
            # Create Clear Cache button
            self.clear_cache_btn = ctk.CTkButton(
                self.buttons_frame,
                text="Clear Cache",
                command=self.clear_cache,
                font=ctk.CTkFont(size=BUTTON_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY),
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                corner_radius=BUTTON_CORNER_RADIUS,
                **RED_BUTTON
            )
            self.clear_cache_btn.pack(side="left", padx=5)
            
            # Create main frame with better styling
            self.main_frame = ctk.CTkFrame(self, corner_radius=15)
            self.main_frame.grid(row=1, column=0, padx=30, pady=(0,30), sticky="nsew")
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(0, weight=1)

            # Create content frame with scrolling
            self.content_frame = ctk.CTkScrollableFrame(
                self.main_frame,
                corner_radius=10,
                fg_color="transparent"
            )
            self.content_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            
            self.upload_label = ctk.CTkLabel(
                self.main_frame, 
                text="Select your watch-history.html file from Google Takeout",
                font=ctk.CTkFont(size=20, family=FONT_FAMILY)
            )
            self.upload_label.grid(row=0, column=0, padx=20, pady=(20,10))
            
            self.upload_button = ctk.CTkButton(
                self.main_frame,
                text="Choose File",
                command=self.upload_file,
                font=ctk.CTkFont(size=BUTTON_FONT_SIZE, weight=FONT_WEIGHTS["bold"], family=FONT_FAMILY),
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                corner_radius=BUTTON_CORNER_RADIUS,
                **BLUE_BUTTON
            )
            self.upload_button.grid(row=1, column=0, padx=20, pady=(0,20))

            # Try to load cached data on startup
            self.load_cached_data()

            # Add protocol for window close
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Center the window on screen
            self.center_window()
            
        except Exception as e:
            error_msg = f"Error initializing application:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            show_error_and_exit(error_msg)

    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_thumbnails(self, video_ids):
        """Load thumbnails for a list of video IDs in parallel."""
        thumbnails = {}
        with ThreadPoolExecutor(max_workers=MAX_THUMBNAIL_WORKERS) as executor:
            future_to_id = {
                executor.submit(self.load_single_thumbnail, video_id): video_id 
                for video_id in video_ids
            }
            for future in future_to_id:
                video_id = future_to_id[future]
                try:
                    thumbnails[video_id] = future.result()
                except Exception as e:
                    print(f"Error loading thumbnail for {video_id}: {e}")
                    thumbnails[video_id] = None
        return thumbnails

    def extract_video_id(self, text, url=''):
        """Extract video ID with optimized patterns."""
        # If we have a URL, try to extract from it first
        if url:
            patterns = [
                r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
                r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})'
            ]
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
        
        # If no URL or no match, try to find a URL in the text
        url_pattern = r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
        match = re.search(url_pattern, text)
        if match:
            return match.group(1)
            
        return None

    def parse_youtube_history(self, file_path):
        try:
            print("\nReading file...")
            file_size = os.path.getsize(file_path)
            print(f"File size: {file_size} bytes")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                print("File opened successfully")
                content = file.read()
                print(f"Read {len(content)} bytes")
                
            print("\nCreating BeautifulSoup parser...")
            soup = BeautifulSoup(content, 'lxml')
            video_entries = []
            
            print("\nSearching for video entries...")
            # Try to find the main content container first
            content_div = (
                soup.find('div', {'class': 'mdl-grid'}) or 
                soup.find('div', {'id': 'content'}) or 
                soup.find('body') or 
                soup
            )
            
            # First try to find all video links (fastest method)
            links = content_div.find_all('a', href=lambda x: x and ('watch?v=' in x or 'youtu.be/' in x))
            print(f"Found {len(links)} video links")
            
            if links:
                # Extract text and URLs from links
                video_entries = []
                for link in links:
                    title = link.get_text().strip()
                    url = link.get('href', '')
                    if title and url:
                        # Clean up the URL
                        if url.startswith('//'):
                            url = 'https:' + url
                        elif not url.startswith('http'):
                            url = 'https://www.youtube.com' + url
                        video_entries.append((title, url))  # Store as tuple of (title, url)
                        print(f"Found video: {title} -> {url}")
            else:
                print("No video links found, trying alternative approach...")
                # Try to find div entries with video titles
                entries = content_div.find_all(['div'])
                print(f"Found {len(entries)} potential div entries")
                
                # Filter entries more efficiently
                video_entries = []
                for entry in entries:
                    text = entry.get_text().strip()
                    if text and not any(text.startswith(prefix) for prefix in [
                        'Watched at', 'Search:', 'Visited', 'Subscribed',
                        'http', 'www.', 'https:', '//'
                    ]):
                        # Try to find a URL in the text
                        url = ''
                        url_match = re.search(r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})', text)
                        if url_match:
                            url = url_match.group(0)
                        video_entries.append((text, url))  # Store as tuple of (title, url)
                        print(f"Found video from text: {text} -> {url}")

            if len(video_entries) == 0:
                raise ValueError("No valid video entries found in the file.")
            
            # Count video occurrences and filter out single views
            video_counts = Counter(video_entries)
            filtered_videos = []
            for (title, url), count in video_counts.most_common():
                if count > 1:
                    filtered_videos.append((title, url, count))
            
            print(f"\nFiltered out {len(video_counts) - len(filtered_videos)} single-view videos")
            print(f"Sample filtered video: {filtered_videos[0] if filtered_videos else 'None'}")
                
            # Create statistics
            stats = {
                'total_videos': len(video_entries),
                'unique_videos': len(set(video_entries)),
                'most_watched': filtered_videos
            }
            
            print("\nStatistics generated:")
            print(f"Total videos watched: {stats['total_videos']}")
            print(f"Unique videos watched: {stats['unique_videos']}")
            print(f"Videos with multiple views: {len(filtered_videos)}")
                
            return stats
            
        except Exception as e:
            error_msg = f"Error in parse_youtube_history: {str(e)}"
            print(f"\nERROR: {error_msg}")
            print(f"Traceback:\n{traceback.format_exc()}")
            raise

    def show_loading_screen(self, message="Loading..."):
        if not self.loading_screen:
            self.loading_screen = LoadingScreen(self.main_frame, message)
            self.loading_screen.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.update()
    
    def hide_loading_screen(self):
        if self.loading_screen:
            self.loading_screen.destroy()
            self.loading_screen = None
            self.update()
    
    def load_cached_data(self):
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    self.display_stats(cached_data)
                    print("Loaded data from cache")
        except Exception as e:
            print(f"Error loading cached data: {e}")
    
    def save_to_cache(self, stats):
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(stats, f)
                print("Saved data to cache")
        except Exception as e:
            print(f"Error saving to cache: {e}")

    def display_stats(self, stats):
        try:
            if not stats:
                raise ValueError("No statistics available to display")
            
            # Hide upload frame
            self.upload_button.grid_remove()
            self.upload_label.grid_remove()
            
            # Show buttons
            self.new_file_btn.pack(side="left", padx=5)
            self.clear_cache_btn.pack(side="left", padx=5)
            
            # Update header with stats
            self.header.configure(
                text=f"YouTube History Recap"
            )
                
            # Store all videos for pagination
            self.all_videos = stats['most_watched']
            self.total_pages = (len(self.all_videos) + self.videos_per_page - 1) // self.videos_per_page
            
            # Create pagination instance with updated total pages
            self.pagination = ModernPagination(
                self.header_frame,
                self.current_page,
                self.total_pages,
                self.display_page
            )
            self.pagination.pack(side="left", expand=True, fill="x", padx=10)
            
            # Display first page
            self.current_page = 0
            self.display_page(0)
                
        except Exception as e:
            error_msg = f"Error displaying statistics: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.show_error(error_msg)

    def on_closing(self):
        if DEBUG:
            print("Application closing...")
        self.quit()

    def upload_file(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("HTML files", "*.html")]
            )
            if file_path:
                # Clear cache before processing new file
                if os.path.exists(self.cache_file):
                    os.remove(self.cache_file)
                    print("Cleared cache file")
                
                self.show_loading_screen("Starting file processing...")
                print("\n=== Starting file processing ===")
                print(f"Selected file: {file_path}")
                
                def process_file():
                    try:
                        self.update_loading_message("Reading file contents...")
                        print("\n--- Parsing file ---")
                        stats = self.parse_youtube_history(file_path)
                        
                        if stats and stats['total_videos'] > 0:
                            self.update_loading_message("Saving data to cache...")
                            self.save_to_cache(stats)
                            self.update_loading_message("Preparing to display results...")
                            print("\n--- Displaying statistics ---")
                            self.after(100, lambda: self.display_stats(stats))
                        else:
                            raise ValueError("No valid statistics were generated")
                            
                    except Exception as e:
                        error_msg = f"Error processing file:\n{str(e)}"
                        print(f"\nERROR: {error_msg}")
                        self.after(0, lambda: self.show_error(error_msg))
                    finally:
                        self.after(0, self.hide_loading_screen)
                
                threading.Thread(target=process_file).start()
                
        except Exception as e:
            error_msg = f"Error in file dialog:\n{str(e)}"
            print(f"\nERROR: {error_msg}")
            self.show_error(error_msg)

    def show_error(self, message):
        try:
            print("\nERROR:", message)
            messagebox.showerror("Error", message)
        except Exception as e:
            print(f"Error showing error dialog: {str(e)}\n{traceback.format_exc()}")

    def clear_cache(self):
        """Clear the application's cache file."""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                print("Cleared cache file")
                # Reset the UI to initial state
                self.upload_button.grid()
                self.upload_label.grid()
                self.new_file_btn.pack_forget()
                self.clear_cache_btn.pack_forget()
                self.header.configure(text="YouTube History Recap")
                
                # Remove old pagination if it exists
                if hasattr(self, 'pagination'):
                    self.pagination.destroy()
                
                # Clear content frame
                for widget in self.content_frame.winfo_children():
                    widget.destroy()
                
                self.all_videos = []
                self.total_pages = 0
                self.current_page = 0
                messagebox.showinfo("Success", "Cache cleared successfully!")
        except Exception as e:
            print(f"Error clearing cache: {e}")
            messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")

    def display_page(self, page_num):
        self.show_loading_screen("Loading page content...")
        
        def load_page():
            try:
                # Clear existing content
                for widget in self.content_frame.winfo_children():
                    widget.destroy()
                    
                self.current_page = page_num
                self.update_loading_message("Creating page layout...")
                
                start_idx = page_num * self.videos_per_page
                end_idx = min(start_idx + self.videos_per_page, len(self.all_videos))
                
                # Get video IDs for this page
                page_videos = self.all_videos[start_idx:end_idx]
                self.update_loading_message(f"Processing videos {start_idx + 1} to {end_idx}...")
                
                video_ids = []
                for video in page_videos:
                    title, url, count = video  # Unpack the video tuple
                    video_id = self.extract_video_id(title, url)
                    if video_id:
                        print(f"Found video ID for '{title}': {video_id}")
                    else:
                        print(f"Warning: Could not extract video ID for '{title}'")
                    video_ids.append(video_id)
                
                # Load all thumbnails in parallel
                self.update_loading_message("Loading video thumbnails...")
                thumbnails = self.load_thumbnails(video_ids)
                
                # Create all video entries at once
                self.update_loading_message("Creating video entries...")
                for i, (video, video_id) in enumerate(zip(page_videos, video_ids)):
                    try:
                        title, url, count = video  # Unpack the video tuple
                        video_entry = VideoEntry(
                            self.content_frame,
                            title,
                            count,
                            video_id,
                            start_idx + i + 1,
                            thumbnails.get(video_id)
                        )
                        video_entry.grid(row=i, column=0, sticky="ew", pady=(0,10))
                        print(f"Created entry for '{title}' with video ID {video_id}")
                    except Exception as e:
                        print(f"Error creating video entry for '{title}': {str(e)}")
                
                # Add a small delay to ensure the loading screen is visible
                self.after(300, self.hide_loading_screen)
                
            except Exception as e:
                error_msg = f"Error loading page: {str(e)}"
                print(error_msg)
                self.after(0, lambda: self.show_error(error_msg))
                self.after(0, self.hide_loading_screen)
        
        # Run page loading in a separate thread
        threading.Thread(target=load_page).start()

    def update_loading_message(self, message):
        if self.loading_screen:
            self.loading_screen.message.configure(text=message)
            self.update()

    def load_single_thumbnail(self, video_id):
        """Load a single thumbnail with timeout."""
        try:
            if not video_id:
                print(f"Warning: No video ID provided for thumbnail")
                return None
                
            print(f"Loading thumbnail for video ID: {video_id}")
            thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"  # Try high quality first
            response = requests.get(thumb_url, timeout=THUMBNAIL_TIMEOUT)
            
            if response.status_code == 404:
                print(f"Maxresdefault not found for {video_id}, trying hqdefault")
                thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"  # Fall back to high quality
                response = requests.get(thumb_url, timeout=THUMBNAIL_TIMEOUT)
                
            if response.status_code == 404:
                print(f"HQdefault not found for {video_id}, trying default")
                thumb_url = f"https://img.youtube.com/vi/{video_id}/default.jpg"  # Fall back to default
                response = requests.get(thumb_url, timeout=THUMBNAIL_TIMEOUT)
            
            if response.status_code == 200:
                img_data = Image.open(BytesIO(response.content))
                # Maintain 16:9 aspect ratio with correct size from settings
                return ctk.CTkImage(light_image=img_data, dark_image=img_data, size=THUMBNAIL_SIZE)
            else:
                print(f"Failed to load thumbnail for {video_id}, status code: {response.status_code}")
            return None
        except Exception as e:
            print(f"Error loading thumbnail for {video_id}: {str(e)}")
            return None

if __name__ == "__main__":
    try:
        if DEBUG:
            print("Starting application in debug mode...")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        app = YouTubeHistoryApp()
        app.mainloop()
    except Exception as e:
        error_msg = f"Application crashed:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        show_error_and_exit(error_msg)
