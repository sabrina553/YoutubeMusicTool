import requests
import math
from system import system
from bs4 import BeautifulSoup


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
             
    def linktofilename(self, link):
        """Convert a link to a filename."""        
        link = link.split("/")        
        if len(link) == 5:  return f"{self.dir_path}/.env/cache/{link[-2]}-{link[-1]}.html"
        if len(link) == 6:  return f"{self.dir_path}/.env/cache/{link[-3]}-{link[-2]}-{link[-1]}.html"
        if len(link) == 7:  return f"{self.dir_path}/.env/cache/{link[-4]}-{link[-3]}-{link[-2]}-{link[-1]}.html"
    
    
    def sample_finder(self, link):
        """get whosampled html for a given song link."""
        
        filename = self.linktofilename(link)
        
        if system.path_exists(self, filename):            
            return filename
        
        response = self.session.get(link)
        if response.status_code == 404:
            print(f"404 - {link} not found.")  
            return None      
       
        with open(filename, 'wb') as f:
            f.write(response.content)

        return filename
        
    
    def parse_sample_main(self, filename):
        """parse from main page of whosampled for given song, the number of samples etc."""
                
        #samples, sampled, covered#
        sampleQuantityData = [0]*3

        with open(filename, 'rb') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        j = []
        for i in soup.find_all("h3" , class_="section-header-title"):            
            i = str(i.contents[0])
            
            i = i.split(' ')
            j.append(i)
            if "samples" in i:
                sampleQuantityData[0] = int(i[3])
            if "Sampled" in i:
                sampleQuantityData[1] = int(i[2])
            if "Covered" in i:
                sampleQuantityData[2] = int(i[2])  
      
        return sampleQuantityData
           
    def sample_main_logic(self, sampleQuantityData, link):  
                      
        url = ["/samples", "/sampled", "/covered"]
        samples = []
        
        n=0        
        if sampleQuantityData[0] > 3: 
            ceiling = math.ceil(sampleQuantityData[0]/16)
            for i in range(ceiling):
                self.sample_finder(f"{link}{url[0]}?cp={i+1}")
                samples.append(self.parse_samples(self.linktofilename(f"{link}{url[0]}?cp={i+1}")))            
            
            del samples[n][0:3]
            n+=ceiling

        if sampleQuantityData[1] > 3:
            ceiling = math.ceil(sampleQuantityData[1]/16)            
            for i in range(ceiling):            
                self.sample_finder(f"{link}{url[1]}?cp={i+1}")                
                samples.append(self.parse_samples(self.linktofilename(f"{link}{url[1]}?cp={i+1}")))
            
            del samples[n][0:3]
            n+=ceiling

        if sampleQuantityData[2] > 3:    
            ceiling = math.ceil(sampleQuantityData[2]/16) 
            for i in range(ceiling):            
                self.sample_finder(f"{link}{url[2]}?cp={i+1}")  
                samples.append(self.parse_samples(self.linktofilename(f"{link}{url[2]}?cp={i+1}")))
            
            del samples[n][0:3]
            n+=ceiling

        samples.append(self.parse_samples(self.linktofilename(link)))
   
    
        return samples
    
    def parse_samples(self,filename):
        """Parse the samples from the cached HTML."""
        with open(filename, 'rb') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        samples = []
        n = 0
        for i in soup.find_all("td", class_="tdata__td1"):
            i = (i.find('a'))
            i = str(i.contents[1])
            i = i.split('"')
            samples.append(i[1])
            
        return samples
    

