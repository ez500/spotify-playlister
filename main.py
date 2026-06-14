import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- CONFIGURATION ---
with open('ids', 'r') as f:
    lines = f.read().splitlines()
CLIENT_ID = lines[0]
CLIENT_SECRET = lines[1]
PLAYLIST_ID = lines[2]


def get_worship_playlist_tracks(playlist_id):
    # 1. Authenticate with the Spotify API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # 2. Fetch the playlist items
    try:
        results = sp.playlist_items(playlist_id)
        tracks = results['items']

        # 3. Handle pagination
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        # 4. Extract song names into a list
        song_titles = []
        for item in tracks:
            track = item['track']
            # Safeguard in case of local files or unavailable tracks
            if track is not None:
                song_titles.append(track['name'])

        # 5. Print ONLY the song titles separated by ", "
        print(", ".join(song_titles))

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    get_worship_playlist_tracks(PLAYLIST_ID)