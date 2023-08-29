import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your Spotify API credentials
SPOTIPY_CLIENT_ID = 'afd65e97488f4e028f3b91e8eafe2766'
SPOTIPY_CLIENT_SECRET = '370721745d0b43a8ab7e098c05f79cd0'
SPOTIPY_REDIRECT_URI = 'https://spotifyprjctbackend.runes121.repl.co'

sp = None


def authenticate():
    global sp
    auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                client_secret=SPOTIPY_CLIENT_SECRET,
                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                scope=['user-read-playback-state'])
    sp = spotipy.Spotify(auth_manager=auth_manager)


def get_main_data():
    current_track = sp.current_playback()
    if current_track is not None:
        artist_names_list = ""
        for artist in current_track['item']['artists']:
            artist_names_list = artist_names_list + artist['name'] + ", "
        artist_names_list = artist_names_list[:-2]
        main_data = {
            "is_playing": True,
            "is_paused": not current_track["is_playing"],
            "track_name": current_track['item']["name"],
            "artist_names": artist_names_list,
            "album_art_url": current_track["item"]["album"]["images"][0]["url"],
            "track_duration": current_track["item"]["duration_ms"],
            "current_progress": current_track["progress_ms"],
            "remaining_ms": current_track["item"]["duration_ms"] - current_track["progress_ms"],
            "playing_on": current_track["device"]["name"],
            "shuffling": current_track["shuffle_state"],
            "repeat_state": current_track["repeat_state"]
        }
        return main_data
    else:
        main_data = {
            "is_playing": False
        }
        return main_data
