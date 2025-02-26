import requests
import configparser
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic, OAuthCredentials

class YouTubeAPI:
    def __init__(self):
        """Initialize the YouTubeAPI class."""
        self.ytm = None
        self.init()

    def get_api_key(self, id):
        """Retrieve the API key from the configuration file."""
        config = configparser.ConfigParser()
        config.read(filenames='.env/config.ini')
        return config['oauth'][id]

    def oauth(self):
        """Authenticate with the YouTube API using OAuth."""
        client_id = self.get_api_key("client_id")
        client_secret = self.get_api_key("client_secret")
        self.ytm = YTMusic(".env/oauth.json", oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))

    def init(self):
        """Initialize the YouTube API."""
        self.oauth()

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
        self.ytm.add_playlist_items(playlistId=pid, videoIds=sid, duplicates=False)


class WhoSampledAPI:
    def __init__(self):
        """Initialize the WhoSampledAPI class."""
        self.session = requests.Session()
        self.session.headers = {
            "Host": "www.whosampled.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "scheme": "https",
            "Accept": "*/*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Referer": "https://www.whosampled.com/",
            "Origin": "https://www.whosampled.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=6",
            "TE": "trailers",
            "Content-Type": "application/json"
        }

    def samples_url(self, data):
        """Construct the URL for samples of a song."""
        data[0] = "-".join(data[0].split())
        data[1] = "-".join(data[1].split())
        return f"https://www.whosampled.com/{data[1]}/{data[0]}/samples"

    def sample_finder(self, link):
        """Find samples for a given song link."""
        response = self.session.get(link)
        if response.status_code == 404:
            response = self.session.get(link[:-8])

        with open('cache.html', 'wb') as f:
            f.write(response.content)

        return self.parse_samples()

    def parse_samples(self):
        """Parse the samples from the cached HTML."""
        with open('cache.html', 'rb') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        samples = []

        for i in soup.find_all("td", class_="tdata__td1"):
            j = (i.find('a'))
            j = str(j.contents[1])
            j = j.split('"')
            samples.append(j[1])
        return samples


class MusicSampler:
    def __init__(self):
        """Initialize the MusicSampler class."""
        self.youtube_api = YouTubeAPI()
        self.whosampled_api = WhoSampledAPI()

    def convert_to_list(self, yay):
        """Convert a single item to a list if necessary."""
        return yay if isinstance(yay, list) else [yay]

    def find_song_samples(self, ids):
        """Find samples for a list of song IDs."""
        samples = []
        for id in ids:
            link_sample = self.whosampled_api.samples_url(self.youtube_api.readable_data(id))
            sample_links = self.whosampled_api.sample_finder(link_sample)
            samples.append(self.youtube_api.song_search(sample_links))
        return samples

    def read_samples(self, links, samples):
        """Read and print samples for a list of song links."""
        for link, sample in zip(links, samples):
            if sample:
                current_song = self.youtube_api.readable_data(link)
                print(f"Songs sampled in {current_song[0]} \n")
                sample_video_ids = [s[0] for s in sample]
                for s in sample:
                    print(f"{s[1]} - {s[2]}")
                print("\n")
                # Uncomment the following line to add samples to a playlist
                #self.youtube_api.add_to_playlist("https://music.youtube.com/playlist?list=PLv9DYoydAiAG9yqDeiAJ-MYUvV0d4i5jd&si=IJcE7Bjo2BDUsL-G", sample_video_ids)

    def main(self):
        """Main function to find and read song samples."""
        link_youtube = "https://music.youtube.com/playlist?list=OLAK5uy_m_zl1RNdUJwiB2Yi1ExSwNQ0Vh3U0-LBQ&si=1b8r7gmgrMzJesz9"  # DAMN.
        ids = self.convert_to_list(self.youtube_api.link_to_id(link_youtube))
        samples = self.find_song_samples(ids)
        self.read_samples(ids, samples)


if __name__ == "__main__":
    sampler = MusicSampler()
    sampler.main()