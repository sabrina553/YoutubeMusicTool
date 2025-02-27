from auth import oauth, unauth
from urllib.parse import urlparse, parse_qs

class YouTubeAPI:
    def __init__(self):
        """Initialize the YouTubeAPI class."""
        
        self.ytm = unauth()
        self.ytmauth = oauth()        
 
    def link_to_id(self, link):
        """Convert a YouTube link to a video or playlist ID."""
        query = urlparse(link)
        if query.hostname == 'youtu.be':
            return query.path[1:]

        if query.path == '/playlist':
            return [track['videoId'] for track in self.ytm.get_playlist(self.playlist_link(link))['tracks']]

        if query.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
            if query.path == '/watch':
                return parse_qs(query.query)['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]

        if query.hostname == 'music.youtube.com':
            if query.path == '/watch':
                return parse_qs(query.query)['v'][0]
        return None

    def playlist_link(self, link):
        """Extract the playlist ID from a YouTube link."""
        query = urlparse(link)
        return parse_qs(query.query)['list'][0]

    def readable_data(self, id):
        """Retrieve readable data for a YouTube video."""
        song_data = self.ytm.get_song(id)
        return [song_data["videoDetails"]["title"], song_data["videoDetails"]["author"], song_data["microformat"]["microformatDataRenderer"]["urlCanonical"]]

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
        self.ytmauth.add_playlist_items(playlistId=pid, videoIds=sid, duplicates=False)

