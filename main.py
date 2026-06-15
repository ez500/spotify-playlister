import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- CONFIGURATION ---
with open('ids', 'r') as f:
    lines = f.read().splitlines()
CLIENT_ID = lines[0]
CLIENT_SECRET = lines[1]
PLAYLIST_ID = lines[2]

# This must match EXACTLY what you put in the Spotify Developer Dashboard
REDIRECT_URI = 'http://127.0.0.1:8888'


def get_worship_playlist_tracks(playlist_id):
    # Authenticate using OAuth with an existing cached token (no browser needed)
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='playlist-read-private',
        open_browser=False,
        cache_handler=spotipy.oauth2.CacheFileHandler(cache_path='.cache')
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    try:
        # Don't use additional_types - let spotipy use the default which returns 'track'
        results = sp.playlist_items(playlist_id)
        tracks = results['items']

        # Handle pagination
        while results.get('next'):
            results = sp.next(results)
            tracks.extend(results['items'])

        # Extract song names
        song_titles = []
        for item in tracks:
            # Try 'track' first, fall back to 'item' for different API response formats
            track = item.get('track') or item.get('item')
            if track is not None and track.get('name'):
                song_titles.append(track['name'])

        # Print results
        if song_titles:
            print("Songs: ")
            print(", ".join(song_titles))
        else:
            print("Songs: ")
            print("(no tracks found)")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    get_worship_playlist_tracks(PLAYLIST_ID)
