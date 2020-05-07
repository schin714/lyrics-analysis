#username and pw for test Genius account
#dappl3
#dAPI4321

import requests
from bs4 import BeautifulSoup

#api url for Genius
base_url = "http://api.genius.com"
#client access token
headers = {'Authorization': 'Bearer Nh1Stv8YTiHStJn7Dv5PedsphgsiNAChcP_9zXAo0gbiZEc6dJR5Xk7MnEWEeO1j'}

song_title = "Hotel California"
artist_name = "Eagles"

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  #html scraping
  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  #use BeautifulSoup to get the text of the page
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #Genius has a div tag with class 'lyrics'
  lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
  return lyrics

if __name__ == "__main__":
  search_url = base_url + "/search"
  data = {'q': song_title}
  #use Requests to get a response from the given search_url with the given params
  response = requests.get(search_url, params=data, headers=headers)
  #Request's function to get the json of the response
  json = response.json()
  song_info = None

  for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == artist_name:
      song_info = hit
      break

  if song_info:
    song_api_path = song_info["result"]["api_path"]
    lyrics = lyrics_from_song_api_path(song_api_path)

    lyricList = lyrics.split()
    lyricDict = {}
    for word in lyricList:
    	if word in lyricDict:
    		lyricDict[word] += 1
    	else:
    		lyricDict[word] = 1

    #sort dict by creating a list of tuples
    sortedLyrics = sorted(lyricDict.items(), key=lambda kv: kv[1])

    for pair in sortedLyrics:
    	print(pair)







