#helper imports
import random
import os
# from .playlist import fetch_all_youtube_videos 
import json

#downloader
from pytube import YouTube

#our client api imports

from oauth2client.tools import argparser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
max_results = 10
rows, columns = os.popen('stty size', 'r').read().split()
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyBP1tLKpaLNYBHg8Ymtc5Fp-cI72m9Y1fw'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query, max_results):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=query,
    part='id,snippet',
    maxResults=max_results
  ).execute()

  return search_response

def nextPage(search_response, query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,                                        developerKey=DEVELOPER_KEY)
    nextPageToken = search_response.get('nextPageToken')
    while ('nextPageToken' in search_response):
        nextPage = youtube.search().list(
        q=query,
        part="id, snippet",
        maxResults=max_results,
        pageToken=nextPageToken
      ).execute()
        search_response['items'] = search_response['items'] + nextPage['items']
        if 'nextPageToken' not in nextPage:
            search_response.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']
        os.system('clear')
        return search_response


def get_vals(search_response):
    videos = []
    vidrec = {}
    playrec = {}
    playlists = []
    # Add each result to the appropriate list, and then display the lists of

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            # videos.append('%s (%s)' % (search_result['snippet']['title'],
            #search_result['id']['videoId']))
            vidrec['id'],vidrec['name'] = search_result['id']['videoId'], search_result['snippet']['title']
            videos.append(json.dumps(vidrec))
        elif search_result['id']['kind'] == 'youtube#playlist':
            # playlists.append('%s (%s)' % (search_result['snippet']['title'],
            #  search_result['id']['playlistId']))
            playrec['id'],playrec['name'] = search_result['id']['playlistId'], search_result['snippet']['title']
            playlists.append(json.dumps(vidrec))
    return videos, playlists #return an array of jesonified records


#show download progress
def progress_check(stream = None, chunk = None, file_handle = None, remaining = None ):#complete
    percent = (100*(file_size-remaining))/file_size
    print("---->> {:00.0f}% downloaded ".format(percent), end="\r")#solve progress 

#file path to save the video
def file_path():#complete
    home = os.path.expanduser('~')
    dpath = os.path.join(home, 'storage', 'downloads')
    return dpath

#the download func
def download(ids):#complete
    """
  :Todo
  		add logic to allow user to choose video quality
  		and choose conversion to mp3
                """
    url = f'https://www.youtube.com/watch?v={ids}'
    video = YouTube(url, on_progress_callback=progress_check)
    vid_type = video.streams.filter(progressive=True, file_extension = "mp4").first()
    global file_size
    file_size = vid_type.filesize
    d = input(f"Proceed to download {file_size/1e+6} mb file (y/n) :")
    if d.lower() == "n":
        os.system("clear")
    elif d.lower() == "y":
        vid_type.download(file_path())
    else:
        print("Sorry did not understand command")
        exit(1)



# user interactions 

def main():
  fonts = ["block","bubble","digital","ivrit","mini","script","shadow","slant","small","smscript","smshadow","smslant","standard"]
  random.shuffle(fonts)
  os.system("clear")
  os.system('echo  "\\e[1;31m\"')
  os.system('echo "\\e[1;32m\"')
  os.system('echo "\\e[1;32m\"')
  os.system('echo "\\e[1;34m          Created By H4CK4BY55 \\e[0m"')
  os.system('echo "\\e[2;32m     we are the league of drunkards \\e[0m"')
  os.system('echo "\\e[2;32m     Winter Sn0w Malibu Glitch ChArlie Koimet \\e[0m"')
  os.system('echo "\\e[1;32m   Mail: hackbytes@protonmail.com \\e[0m"')
  print()
  name = input("Enter Video to search q to quit:")
  if name.lower() == "q":
      print("exiting")
      exit()
  search_response = youtube_search(name, max_results)
  while True:
    # videos, playlists = youtube_search(name, 10)
    videos, playlists = get_vals(search_response)
    for key, i in enumerate(videos):
      d = json.loads(i)
      os.system(f'echo "{key}|\\e[2;32m {d["name"]}\\e[0m"')
      print("_"*int(columns))
      #print(f"{key}- {d['name']}")
    n = input("enter m for more number to download  s to search again: ")
    try:
      if n.lower() == "m":
        search_response = nextPage(search_response, name)
      elif n.lower() == "s":
        os.system("clear")
        main()
      else:
        num = int(n)
        vids = [json.loads(i) for i in videos]
        vid_file = vids[int(num)]
        download(vid_file['id'])
    except Exception as e:
        print("Sorry n  or number" + str(e))
        exit(0)


if __name__ == "__main__":
    main()
