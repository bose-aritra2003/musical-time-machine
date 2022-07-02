from bs4 import BeautifulSoup
import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

date = input("What year would you like to travel to in YYYY-MM-DD format ? ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")
extract_names = soup.find_all('h3', id='title-of-a-story', class_='a-no-trucate')
song_list = [name.getText().strip() for name in extract_names]

print("\nThese are the songs that are on the Hot 100 for the date you entered:")
for song in song_list:
    print(song)
print()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print("Authentication successful!")
print()

songs_uri = []
year = date[:4]
result = 0

print("Searching selected songs on Spotify...")
# Song searching
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"\"{song}\" not found on Spotify. Skipping...")
print()

print("Creating playlist...")
# Creating playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
print("Done!")
print("Playlist URL: https://open.spotify.com/playlist/{}".format(playlist["id"]))
