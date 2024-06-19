# Audio Features Extractor 🎶

## Description
This application is a tool to extract audio features from songs in a Spotify playlist. Extracted audio features include danceability, energy, key, loudness, and more. The data can be downloaded in CSV format after extraction.

## Usage
1. **Input Spotify Playlist Information**
   - Enter the `Username` and `Playlist ID` from your Spotify account and the playlist you want to analyze.

2. **Extracted Features**
   - The application will extract audio features for each song in the specified playlist.
   - Extracted features include:
     - `id`: Spotify ID of the song
     - `title`: Song title
     - `first_artist`: Main artist name
     - `all_artists`: All artists involved in the song
     - `danceability`, `energy`, `key`, `popularity`, `streams`, `loudness`, `mode`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_ms`, `time_signature`

3. **Download Data**
   - After extraction is complete, the results can be downloaded in CSV format using the "Download as CSV" button.

## Installation and Local Usage
To run this application locally, make sure you have installed all required Python packages listed in `requirements.txt`. You can install them by running the following command:
```
pip install -r requirements.txt
```

To start the application, run the `main.py` script:
```
python main.py
```

## License
Specify licensing information here (if applicable).

## Contact
For questions or feedback, please contact [Your Name] at [Your Email].


### Notes:

- Make sure to replace the `Description` section with a brief description of what the application does and its capabilities.
- In the `Extracted Features` section, adjust it to include the specific features extracted by your script.
- In the `Installation and Local Usage` section, tailor it to match the installation and usage steps of your script, including package installation with `pip`.
- Don't forget to include appropriate licensing information if you have specific licensing for your project.
- In the `Contact` section, provide your contact information for further inquiries.

This guide will help create an informative README that assists users in understanding how to use and contribute to your project effectively.
