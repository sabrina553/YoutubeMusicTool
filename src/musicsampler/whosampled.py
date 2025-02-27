import requests
from bs4 import BeautifulSoup
from system import system


class WhoSampledAPI:
    def __init__(self):
        """Initialize the WhoSampledAPI class."""
        self.dir_path = system.current_directory(self)
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
        return f"https://www.whosampled.com/{data[1]}/{data[0]}"
    
    
    def sample_finder(self, link, data):
        """Find samples for a given song link."""

        filename = f"{self.dir_path}/.env/cache/{data[1]}-{data[0]}-sample.html"
        if system.path_exists(self, filename):
            return self.parse_samples(filename)
        
        response = self.session.get(link)
        if response.status_code == 404:
            response = self.session.get(link[:-8])                
        
        with open(filename, 'wb') as f:
            f.write(response.content)

        return self.parse_samples(filename)
    
    def parse_sample_main(self, link, data):
        """parse from main site"""
        filename = f"{self.dir_path}/.env/cache/{data[1]}-{data[0]}.html"
        with open(filename, 'rb') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        j = []
        for i in soup.find_all("h3" , class_="section-header-title"):            
            i = str(i.contents[0])
            i = i.split(' ')
            j.append(i)
        #samples, sampled, covered#
        j = j[0][3],j[1][2],j[2][2]
        print(j)


    def parse_samples(self,filename):
        """Parse the samples from the cached HTML."""
        with open(filename, 'rb') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        samples = []

        for i in soup.find_all("td", class_="tdata__td1"):
            i = (i.find('a'))
            i = str(i.contents[1])
            i = i.split('"')
            samples.append(i[1])
        return samples

    def main(self):
        #self.sample_finder("https://www.whosampled.com/The-Notorious-B.I.G./Hypnotize/",   ["Hypnotize", "The Notorious B.I.G."])
        self.parse_sample_main("https://www.whosampled.com/The-Notorious-B.I.G./Hypnotize/",   ["Hypnotize", "The Notorious B.I.G."])





WhoSampledAPI().main()