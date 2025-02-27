import requests
from bs4 import BeautifulSoup

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
    
    def parse_sample_finder(self):
        print()

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
