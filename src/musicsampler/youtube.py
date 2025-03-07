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
            song_instance.populate_from_id(i['videoId'])
            self.songs.append(song_instance)           

        return self
      
class song:
    def __init__(self):
        self.ytm = unauth()
        self.songData = None
        self.videoID = None
        self.title = None
        self.artist = None       
        self.album = None
        self.albumID = None
        self.duration = None
        self.category = None
        self.whoSampledLink = None
        self.samples = None
        self.sampled = None
        self.covered = None     
        self.samplesYoutubeID = []      
        self.sampledYoutubeID = None       
        self.samplesCoveredID = None  
        self.samplesSong = [] 
    
    def populate_from_id(self, id):        
        dict = self.ytm.get_song(id)
        self.songData = dict
        self.videoID = dict['videoDetails']['videoId']
        self.title = dict['videoDetails']['title']
        self.artist = dict['videoDetails']['author']            
        self.duration = dict['videoDetails']['lengthSeconds']        
        self.category = dict['microformat']['microformatDataRenderer']['category']
        self.samples_url()
        return self
    
    def readSamples(self):
        print(f"Sampled in {self.title}")
        for i in self.samplesSong:
            print(i.title)         
    
    def samples_url(self):
        """Construct the URL for samples of a song."""
        Artist = "-".join(self.artist.split())
        Title = "-".join(self.title.split())       
        self.whoSampledLink = f"https://www.whosampled.com/{Artist}/{Title}"
        return self 
    
    def samplesIDtoObject(self):        
        for i in self.samplesYoutubeID:
            song_instance = song()            
            self.samplesSong.append(song_instance.populate_from_id(i))
                     

class YouTubeAPI:
    def __init__(self):
        """Initialize the YouTubeAPI class."""        
        self.ytm = unauth()
        self.ytmauth = oauth()  
        self.song = song() 
        self.playlist = playlist()     
 
    def get_song(self, id):
        return self.ytm.get_song(id)
    
    def song_search(self, query, song):
        """Search for songs on YouTube."""        
        #for i in song.samples:
        a = self.ytm.search(query=query, filter="songs", limit=1, ignore_spelling=True)
        if len(a) == 1:
            song.samplesYoutubeID.append(a[0]['videoId'])
        elif len(a) > 1:
            song.samplesYoutubeID.append(a[1]['videoId'])
    
    def playlist_link(self, link):
        """Extract the playlist ID from a YouTube link."""
        query = urlparse(link)
        return parse_qs(query.query)['list'][0]
    
    def playlist_data(self, id):        
        return self.ytmauth.get_playlist(id)
            
    def create_playlist(self, title, description, songs):
        return self.ytmauth.create_playlist(title=title, description=description, songs=songs)
    
    def link_to_song_object(self, link):
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
        
        return self.song.populate_from_id(temp)
        
    def add_to_playlist(self, pid, sid):
        """Add songs to a YouTube playlist."""
        pid = self.playlist_link(pid)
        print(len(sid))
        for i in range(0, len(sid), 20):
        # call our helper to process a sub list            
            self.ytmauth.add_playlist_items(playlistId=pid, videoIds=sid[i:i+20], duplicates=False)

   
        