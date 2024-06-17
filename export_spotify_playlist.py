import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import re

# Spotify credentials
CLIENT_ID = 'b5d4c41cbe694ba994ea20bc9ba7d782'
CLIENT_SECRET = '036f88539bf9471a84a13efb0296be0d'
REDIRECT_URI = 'http://localhost:8888/callback/'

# Define the scope
scope = 'playlist-read-private'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

# Function to get playlist tracks
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Helper function to debug playlist ID
def print_playlist_info(playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
        print(f"Playlist Name: {playlist['name']}")
        print(f"Playlist ID: {playlist['id']}")
        print(f"Total Tracks: {playlist['tracks']['total']}")
    except Exception as e:
        print(f"Error: {e}")

# Function to extract playlist ID from URL
def extract_playlist_id(url):
    pattern = r"playlist/([a-zA-Z0-9]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Spotify URL")

# Provided playlist URL
playlist_url = 'https://open.spotify.com/playlist/7M8kf5w2HD6Rw5VzsgqmSd?si=b541ee1e13ee4d91'

# Extract the playlist ID from the URL
playlist_id = extract_playlist_id(playlist_url)

# Print playlist info for debugging
print_playlist_info(playlist_id)

# Get the playlist tracks
tracks = get_playlist_tracks(playlist_id)

# Process the tracks
track_data = []
for item in tracks:
    track = item['track']
    track_data.append({
        'Track Name': track.get('name', 'N/A'),
        'Artist': ', '.join([artist['name'] for artist in track['artists']]),
        'Album': track['album']['name'],
        'Release Date': track['album']['release_date'],
        'Track URL': track['external_urls'].get('spotify', 'N/A') if 'external_urls' in track else 'N/A'
    })

# Create a DataFrame and export to Excel
df = pd.DataFrame(track_data)
df.to_excel('spotify_playlist.xlsx', index=False)

print('Playlist exported successfully!')