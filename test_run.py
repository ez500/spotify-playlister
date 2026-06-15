import sys

sys.stdout = open('run_output.txt', 'w', encoding='utf-8')
sys.stderr = sys.stdout

print("Script started", flush=True)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

print("Imports done", flush=True)

with open('ids', 'r') as f:
    lines = f.read().splitlines()
CLIENT_ID = lines[0]
CLIENT_SECRET = lines[1]
PLAYLIST_ID = lines[2]

print("Config set", flush=True)

try:
    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    print("Auth manager created", flush=True)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("Spotify client created", flush=True)

    print("Fetching playlist items...", flush=True)
    results = sp.playlist_items(PLAYLIST_ID)
    print(f"Results type: {type(results)}", flush=True)
    print(f"Results keys: {list(results.keys())}", flush=True)

    items = results['items']
    print(f"Got {len(items)} items", flush=True)

    song_titles = []
    for i, item in enumerate(items):
        track = item.get('track')
        if track is not None and track.get('name'):
            song_titles.append(track['name'])
            print(f"  [{i}] {track['name']}", flush=True)
        else:
            print(f"  [{i}] No track (track=None or name=None)", flush=True)

    print(f"\nSong titles ({len(song_titles)}):")
    print(", ".join(song_titles))

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}", flush=True)
    import traceback

    traceback.print_exc(file=sys.stdout)
    sys.stdout.flush()

print("Script finished", flush=True)
sys.stdout.close()
