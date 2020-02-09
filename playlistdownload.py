from pytube import Playlist
import os
def downplay():
    playlist = Playlist('https://m.youtube.com/playlist?list=PL1H1sBF1VAKVzeGHJCUIaI54y_UzP0Qlo')
    size =0
    total = 0
    home = os.path.expanduser('~')
    dpath = os.path.join(home, 'storage', 'downloads')
    print(f"do you want to download {playlist.title()}")
    for vid in playlist.videos:
        #print(size)
        if total < 4:
            files = vid.streams.filter(progressive=True).first()
            #files.download(dpath)
            total += 1
        else:
            break
   # size = size/1e+6
    #print(f"Number of videos in playlist:{len(playlist.video_urls)} size:{size}")
    
downplay()
