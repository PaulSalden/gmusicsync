from bs4 import BeautifulSoup
from gmusicapi import Mobileclient
import requests
import details

PLAYLISTNAME = "Global Dance Chart 40"

def get_apiclient():
	api = Mobileclient()
	api.login(details.username, details.password, Mobileclient.FROM_MAC_ADDRESS)
	return api

def get_clearedplaylistid(api, name):
	for playlist in api.get_all_user_playlist_contents():
		if playlist["name"] != name:
			continue

		for entry in playlist["tracks"]:
			api.remove_entries_from_playlist(entry["id"])
		return playlist["id"]

def addsongtoplaylist(api, playlistid, artist, track):
	query = " ".join((artist, track))
	result = api.search(query, max_results=1)["song_hits"]
	if result:
		songid = result[0]["track"]["storeId"]
		api.add_songs_to_playlist(playlistid, songid)

def get_gdc():
	result = requests.get("http://globaldancechart.com/charts/")
	c = result.content
	soup = BeautifulSoup(c)
	artists = [t.get_text() for t in soup.find_all("p", "artist")]
	tracks = [t.get_text() for t in soup.find_all("p", "track")]
	return zip(artists, tracks)

def main():
	api = get_apiclient()
	pid = get_clearedplaylistid(api, PLAYLISTNAME)
	gdc = get_gdc()
	for artist, track in gdc:
		addsongtoplaylist(api, pid, artist, track)

if __name__ == "__main__":
	main()

