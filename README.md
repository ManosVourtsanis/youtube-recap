# YouTube History Recap

A modern desktop application that analyzes your YouTube watch history and provides insights into your most-watched videos. Built with Python and CustomTkinter for a beautiful, native-looking interface.

## Features

- Analyze your YouTube watch history from Google Takeout
- Display video thumbnails and titles
- Show watch counts for each video
- Modern, responsive UI with dark mode support
- Pagination for easy navigation
- Cache support for faster subsequent loads
- High-quality video thumbnails
- Direct links to YouTube videos

## Installation

### Option 1: Using the Executable (Recommended)

1. Download the latest release from the releases page
2. Extract the ZIP file
3. Run `YouTube History Recap.exe`

### Option 2: Running from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-history-recap.git
   cd youtube-history-recap
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/MacOS
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Launch the application
2. Click "Load New File" or "Choose File"
3. Select your `watch-history.html` file from Google Takeout
4. Wait for the analysis to complete
5. Browse through your most-watched videos
6. Click on thumbnails or titles to open videos in your browser

## Getting Your YouTube History

1. Go to [Google Takeout](https://takeout.google.com/)
2. Select "YouTube" from the list of services
3. Choose "YouTube and YouTube Music"
4. Click "Next step"
5. Choose your export options (HTML format recommended)
6. Click "Create export"
7. Download the ZIP file
8. Extract and locate the `watch-history.html` file

## Building the Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build command:
   ```bash
   pyinstaller --clean "YouTube History Recap.spec"
   ```

3. Find the executable in the `dist` folder

## Requirements

- Python 3.8 or higher
- customtkinter==5.2.2
- beautifulsoup4==4.12.3
- lxml==5.1.0
- Pillow==10.2.0
- requests==2.31.0

## Development

The project structure:
```
youtube-history-recap/
├── app.py              # Main application code
├── settings.py         # Configuration settings
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the beautiful UI components
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Pillow](https://pillow.readthedocs.io/) for image processing