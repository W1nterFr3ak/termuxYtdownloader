#helper imports
import os
import argparse
import json

#downloader
from pytube import YouTube

#our client api imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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

  videos = []
  vidrec = {}


  # Add each result to the appropriate list, and then display the lists of
  
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      # videos.append('%s (%s)' % (search_result['snippet']['title'],
      #                            search_result['id']['videoId']))
      vidrec['id'],vidrec['name'] = search_result['id']['videoId'], search_result['snippet']['title']
      videos.append(json.dumps(vidrec))


  return videos #return an array of jesonified records

#show download progress
def progress_check(stream = None, chunk = None, file_handle = None, remaining = None ):
  percent = (100*(file_size-remaining))/file_size
  print("{:00.0f}% downloaded ".format(percent))#solve progress 

#file path to save the video
def file_path():
  home = os.path.expanduser('~')
  dpath = os.path.join(home, 'storage', 'downloads')
  return dpath

#the download func
def download(ids):
  """
  :Todo
  		add logic to allow user to choose video quality
  		and choose conversion to mp3
  """
  print(ids)
  url = f'https://www.youtube.com/watch?v={ids}'
  video = YouTube(url, on_progress_callback=progress_check)
  vid_type = video.streams.filter(progressive=True, file_extension = "mp4").first()
  
  global file_size
  file_size = vid_type.filesize
  print(file_path())
  vid_type.download(file_path())




if __name__ == '__main__':
  name = input("Enter Video to search :")
  videos = youtube_search(name, 10)
  for key, i in enumerate(videos):
    d = json.loads(i)
    print(f"{key}- {d['name']}")

  c = True
  while c:
   	try:
   		num = input("Input t he number of video to download : ")
   		vids = [json.loads(i) for i in videos]
   		file = vids[int(num)]
   		c = False
   		download(file['id'])

   		
   		print("thankyou")
   	except Exception as e:
   		print ("please input a number: " )

    
    

