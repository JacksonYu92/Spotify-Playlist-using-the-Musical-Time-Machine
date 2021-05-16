import spotify as spotify
from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


client_id = os.environ["SPOTIFY_CLIENT_ID"]
client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               )
                     )

user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in the format YYYY-MM-DD: \n")
url = "https://www.billboard.com/charts/hot-100"
response = requests.get(f"{url}/{date}")
hot_100_page = response.text

soup = BeautifulSoup(hot_100_page, "html.parser")
# soup.prettify()
songs = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in songs]
print(song_names)

song_uris = []

year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)