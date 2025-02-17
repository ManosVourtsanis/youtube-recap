# YouTube Watch History Analyzer  

A web application that parses your YouTube watch history from Google Takeout, sorts by the most viewed videos, and displays them in a paginated UI with thumbnails.

## Steps to get your youtube history

1. Go to [Google Takeout](https://takeout.google.com/settings/takeout?pli=1)
2. Scroll down and select "YouTube and YouTube Music"
3. Click "Deselect all" and enable only "History"
4. Scroll down and click "Next step"
5. Under "Delivery method", select "Download file" or email
6. Choose .zip as the file type and click "Create Export"
7. Once the export is ready, download and extract the .zip file
8. Locate the file named watch-history.html inside the extracted folder: Takeout\YouTube and YouTube Music\history
9. Move watch-history.html to the data/ folder in your project directory
10. Rename it to takeout.html just for no reason

## Steps to run the project

1. Clone the project
2. Move the takeout.html file to the /data directory
3. Run the parse_history.py
4. Run the app.py
5. Open your localhost to enjoy the results

Hope you enjoy it!!!