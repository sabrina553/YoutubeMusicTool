from auth import oauth, unauth
from urllib.parse import urlparse, parse_qs

class playlist:    
    def __init__(self):    
        self.ytmauth = oauth() 
        self.url = None
        self.id = None
        self.playlistData = None

        self.title = None
        self.songs = []

        self.trackLength = None
        self.owned = None
        self.privacy = None
        self.description = None     

    def populateFromLink(self, link):        
        self.url = link
        self.id = YouTubeAPI.playlist_link(self, self.url)
        self.playlistData = YouTubeAPI.playlist_data(self, self.id)
        
        self.title = self.playlistData['title']
        self.trackCount = self.playlistData['trackCount']
        self.owned = self.playlistData['owned']
        self.privacy = self.playlistData['privacy']
        self.description = self.playlistData['description']
        
        for i in self.playlistData['tracks']:                                        
            song_instance = song()
            song_instance.populate_from_playlist(i)
            self.songs.append(song_instance)           

        return self
      
class song:
    def __init__(self):
        self.songData = None
        self.videoID = None
        self.title = None
        self.artist = None
        self.artistID = None
        self.album = None
        self.albumID = None
        self.isExplicit = None
        self.duration = None
        self.liked = None
        self.inLibrary = None
        self.duration = None
        self.category = None
        self.samples = None
        self.sampled = None
        self.covered = None
            
    def populate_from_playlist(self, dict):
        self.songData = dict
        self.videoID = dict['videoId']
        self.title = dict['title']
        self.artist = dict['artists'][0]['name']
        self.artistID = dict['artists'][0]['id']
        self.album = dict['album']['name']
        self.albumID = dict['album']['id']
        self.isExplicit = dict['isExplicit']
        self.duration = dict['duration_seconds']
        self.liked = dict['likeStatus']
        self.inLibrary = dict['inLibrary']              
        return self 
    
    def populate_from_song(self, dict):
        self.songData = dict
        self.videoID = dict['videoDetails']['videoId']
        self.title = dict['videoDetails']['title']
        self.artist = dict['videoDetails']['author']
        #self.artistID
        #self.album
        #self.albumID
        #self.isExplicit        
        self.duration = dict['videoDetails']['lengthSeconds']
        #self.liked
        #self.inlibrary
        self.category = dict['microformat']['microformatDataRenderer']['category']
        return self


class YouTubeAPI:
    def __init__(self):
        """Initialize the YouTubeAPI class."""        
        self.ytm = unauth()
        self.ytmauth = oauth()  
        self.song = song() 
        self.playlist = playlist()     
 
    def link_to_id(self, link):
        """Convert a YouTube link to a video or playlist ID."""
        query = urlparse(link)        

        if query.path == '/playlist':            
            instance = self.playlist.populateFromLink(link)
            return [song_obj for song_obj in instance.songs]            
            #return [track['videoId'] for track in self.ytm.get_playlist(self.playlist_link(link))['tracks']]

        if query.hostname == 'youtu.be':
            temp =  query.path[1:]

        if query.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com',  'music.youtube.com'):
            if query.path == '/watch':
                temp = parse_qs(query.query)['v'][0]
            if query.path[:7] == '/embed/':
                temp =  query.path.split('/')[2]
            if query.path[:3] == '/v/':
                temp = query.path.split('/')[2]
        
        return self.song.populate_from_song(self.ytm.get_song(temp))
        
    
    def playlist_link(self, link):
        """Extract the playlist ID from a YouTube link."""
        query = urlparse(link)
        return parse_qs(query.query)['list'][0]
    
    """
    def readable_data(self, id):
        #Retrieve readable data for a YouTube video.
        song_data = self.ytm.get_song(id)
        return [song_data["videoDetails"]["title"], song_data["videoDetails"]["author"], song_data["microformat"]["microformatDataRenderer"]["urlCanonical"]]
    """
        
    def song_search(self, my_list=[]):
        """Search for songs on YouTube."""
        b = []
        for i in my_list:
            a = self.ytm.search(query=i, filter="songs", limit=1, ignore_spelling=True)
            if len(a) == 1:
                b.append([a[0]['videoId'], a[0]['title'], a[0]['artists'][0]['name'], a[0]['artists'][0]['id']])
            elif len(a) > 1:
                b.append([a[1]['videoId'], a[1]['title'], a[1]['artists'][0]['name'], a[1]['artists'][0]['id']])
        return b

    def add_to_playlist(self, pid, sid):
        """Add songs to a YouTube playlist."""
        pid = self.playlist_link(pid)
        print(len(sid))
        for i in range(0, len(sid), 20):
        # call our helper to process a sub list            
            self.ytmauth.add_playlist_items(playlistId=pid, videoIds=sid[i:i+20], duplicates=False)


    def create_playlist(self, title, description, songs):
        return self.ytmauth.create_playlist(title=title, description=description, songs=songs)

    
    def playlist_data(self, id):        
        return self.ytmauth.get_playlist(id)
        
    

"""

if __name__ == "__main__":
    
    link = "https://music.youtube.com/playlist?list=OLAK5uy_nFiS1SeXBnJII-kBfpg7kGRB0JeE_tot8"
    sampler = playlist()
    sampler.populateFromLink(link)
    
    for song_obj in sampler.songs:        
        print(song_obj.videoID)
"""