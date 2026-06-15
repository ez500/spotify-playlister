import spotipy
from spotipy.oauth2 import SpotifyOAuth
import traceback
import sys

# Write everything to a file to avoid terminal capture issues
log = open('debug_log.txt', 'w', encoding='utf-8')

log.write("=== DEBUG START ===\n")
log.flush()

with open('ids', 'r') as f:
    lines = f.read().splitlines()
CLIENT_ID = lines[0]
CLIENT_SECRET = lines[1]
PLAYLIST_ID = lines[2]
REDIRECT_URI = 'http://127.0.0.1:8888'

try:
    log.write("Creating auth manager...\n")
    log.flush()
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='playlist-read-private',
        open_browser=False
    )
    log.write("Auth manager created\n")
    log.flush()

    log.write("Creating Spotify client...\n")
    log.flush()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    log.write("Spotify client created\n")
    log.flush()

    log.write("Fetching playlist metadata...\n")
    log.flush()
    playlist = sp.playlist(PLAYLIST_ID, fields='name,tracks(total)')
    log.write(f"Playlist: {playlist}\n")
    log.flush()

    log.write("Fetching playlist items...\n")
    log.flush()
    results = sp.playlist_items(PLAYLIST_ID)

    log.write(f"Results keys: {list(results.keys())}\n")
    log.write(f"Total items in results: {len(results.get('items', []))}\n")
    log.flush()

    items = results['items']
    for i, item in enumerate(items):
        log.write(f"\n--- Item {i} ---\n")
        log.write(f"Item type: {type(item)}\n")
        log.write(f"Item keys: {list(item.keys())}\n")
        track = item.get('track')
        log.write(f"Track is None: {track is None}\n")
        log.write(f"Is local: {item.get('is_local')}\n")
        if track:
            log.write(f"Track name: {track.get('name')}\n")
            log.write(f"Track type: {type(track)}\n")
            log.write(f"Track keys (first 20): {list(track.keys())[:20]}\n")
        log.flush()

    # Handle pagination
    page_count = 1
    while results.get('next'):
        log.write(f"Fetching page {page_count + 1}...\n")
        log.flush()
        results = sp.next(results)
        items.extend(results['items'])
        log.write(f"Total items now: {len(items)}\n")
        log.flush()
        page_count += 1

    log.write(f"\n=== Total items fetched: {len(items)} ===\n")
    log.flush()

except Exception as e:
    log.write(f"ERROR: {type(e).__name__}: {e}\n")
    log.flush()
    traceback.print_exc(file=log)
    log.flush()

log.write("=== DEBUG END ===\n")
log.close()