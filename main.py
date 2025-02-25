import requests

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic, OAuthCredentials

#https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python :)
#turn url into video ID for search Query
def linkTOID(Link):   
    query = urlparse(Link)    
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if query.path == '/watch':            
            p = urlparse(query.query)            
            return p[2][2:]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    if query.hostname in ('music.youtube.com'):
        if query.path == '/watch':            
            p = urlparse(query.query)   
            p = p[2][2:].partition("&")
            return p[0]        
    # fail?
    return None 

def ReadableData(ID):    
    songData = ytm.get_song(ID)    
    #readable list
    readableSuggestions = [songData["videoDetails"] ["title"], songData["videoDetails"] ["author"], songData["microformat"] ["microformatDataRenderer"]["urlCanonical"]]
    return readableSuggestions

def samplesUrl(ID):     
    data = ReadableData(ID)
    #clean data for url
    data[0] = "-".join(data[0].split())
    data[1] = "-".join(data[1].split())
    #create url
    return f"https://www.whosampled.com/{data[1]}/{data[0]}/samples"    

def sampleFinder(Link):     
    session = requests.Session()
    session.headers = {
        "Host": "www.whosampled.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "scheme":"https",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.whosampled.com/",
        "Cookie": "am_gpp=DBACPeA~CQNVSEAQNVSEAAuACAENBeFsAP_gAEPgAAwIKVsR9G9GRSFj8H53IMskII0PwVhAakAhBgCAE-ABCJOEPIwUhCA4AAzCIiACGRIAODQAAAEAHAAQQEAAYIABIADMAEAQIABKIABAAAIBIEAQAAwAgAAgEAAAgGAEAAQBiAQNAZIARMyAggAGEVAQKAAAAAAAAAAAAAAAQAAAQAAIACgAAAAAAAAAAAAAQBAIAAAAAAAAAAAAAAAAABAAAAAAAAAAAACCbwAJBoREABZEBIQCBBBAABEEAQAEAAIAAAgIIAAAgQBCQMABQgIgAAAgAAAAEAAAAgAAAAAAAIAABAAECAACAAKAAAACAACAAAQAAAASAAEAAIAIAAIAAAAAAABAAAAYAAAAAQAEBAgAAQIAAQAAiAAAAAAAAAAAAAAAAAAEAACAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAQAA.f_wACHwAAAAA~1---~BqgAAAAAAgA; am_gpp_cmp_version=v2test; euconsent-v2=CQNVSEAQNVSEAAuACAENBeFsAP_gAEPgAAwIKVsR9G9GRSFj8H53IMskII0PwVhAakAhBgCAE-ABCJOEPIwUhCA4AAzCIiACGRIAODQAAAEAHAAQQEAAYIABIADMAEAQIABKIABAAAIBIEAQAAwAgAAgEAAAgGAEAAQBiAQNAZIARMyAggAGEVAQKAAAAAAAAAAAAAAAQAAAQAAIACgAAAAAAAAAAAAAQBAIAAAAAAAAAAAAAAAAABAAAAAAAAAAAACCb0EgABYADoAKAAqABcADgAIAASAAygBoAGoAOAAeABEACOAEwAKoAXAAxABoAD0AH4AQgAjgBOACtAGGAMsAaIA5wB3AD4AH6AQCAg4CEAEWAIwAR0AkoBKQCggFiAL6Aa8A4gB1ADtgHtAP6Af8BDoCLwEiAJiATKAnYBQ4CkwFSgLYgXkBeYDFgGSAMsAZmA0YBpoDXgG3gNzAfIA_cCN4E3gAAAAA.f_wACHwAAAAA; _ga_TB5P9YFDE5=GS1.1.1740472223.3.1.1740472906.30.0.0; _ga=GA1.1.217427417.1740378066; _pubCommonId=a8173cab-9573-4089-a364-dce42844ddd5; _pubCommonId_cst=0SxuLFws%2Bg%3D%3D; _lr_env_src_ats=false; _au_1d=AU1D-0100-001740378457-JZVBSFVI-YY6W; mv_cmp_version=v2; am_tokens={%22mv_uuid%22:%2270e57d20-f278-11ef-90a4-8d785966623e%22%2C%22version%22:%22eu-v1%22}; am_tokens_eu-v1={%22mv_uuid%22:%2270e57d20-f278-11ef-90a4-8d785966623e%22%2C%22version%22:%22eu-v1%22}; _scor_uid=a9285613754f4d2d94cc869c596ffcb6; cto_bundle=ddY49V9pTG9LUUxyaTVrciUyQlE0eFQ2MFZzbno0RGMlMkJ4SU1JZ0VJUHlra2JhOVVYT2ZXOGFxZTZ0MUhUMmNGRXFRQ05ieDhUT1VWMjhVOXNIZm5SV29HclhMY01wd0pxU0ZDV1VGSEJIdllqaGZyR3NFcFB0Wmdia2Y1SjlPS0hrODJFMUgzalRZSjRaUmxYeTVmJTJGMDU4VGFOc1ElM0QlM0Q; __gads=ID=ec1a106953676285:T=1740378460:RT=1740472868:S=ALNI_MakdSWCiGAicmKPjNoS4R_hqii8pg; __gpi=UID=00000ff2afb42ef9:T=1740378460:RT=1740472868:S=ALNI_MZhdxOkaB8e0dHneqnGNADcb2klHA; __eoi=ID=eaa7e02c3589569e:T=1740378460:RT=1740472868:S=AA-AfjZIdQCgahwvxADWOc6EiuyT; csrftoken=KivTA1E8TLoSIT0XW8p4M2IsmcYlgLET; _ga_FVWZ0RM4DH=GS1.1.1740472263.6.1.1740472868.60.0.0; __stripe_mid=e00dfd36-7e1f-42f7-a4bd-776c74529e08f21099; __qca=P0-338451626-1740378811956; cf_clearance=ZKrsPWpz38.m3ag03SxtflNH9dF972iIM3XgZKGRJV8-1740472223-1.2.1.1-cHOJxjrlbAAUu4YjmUkmJc._S9cU4zsX6iRtaUldJ94SHW3k6phJw_NKDRNsLwJmgv84ZgO4I0St.nSwmGcKCKWwIwCf.xz4fEHh04vmtb7FLqrIrb5vyfzvocajlaQBNpkwbHIMNdiWPJZzMX3ByQispuOA4B0nNqt70Kcmz3Ti8enpiE6KzfSighRNJkl_lU6zpgmMFaoLtXHc55y.eyMV8x.rI68jYHuxMg43BDt0mtAyYZWIpqNRJ4PvUbgFcnCqASj9vwGpwpzDFA.qLHQh8kagUG.TuQ51AqwBFYE; _lr_retry_request=true; mediavine_session={%22depth%22:10%2C%22referrer%22:%22https://www.google.com/%22%2C%22wrapperVersionGroup%22:{%22version%22:%223.10.70-creativeErrors.1%22%2C%22name%22:%223.10.70-creativeErrors.1-beta-test%22}%2C%22s2sVersionGroup%22:{%22version%22:%22production%22%2C%22name%22:%22production%22}}",
        "Origin": "https://www.whosampled.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=6",
        "TE": "trailers",
        "Content-Type":"application/json"            
    }
    
    response = session.get(Link)  
      
    with open('cache.html', 'wb') as f:
        f.write(response.content)
    
    
    samples = soup()
    return samples

def soup():
    with open('cache.html', 'rb') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')    
    samples = []   
    """ FOR original link, needs changes for /samples
    for link in soup.find_all('tr'):
        a = link.find('a')         
        a = str(a.contents[1])        
        a = a.split('"')
        samples.append(a[1])
    return samples
    """
    for i in soup.find_all("td", class_="tdata__td1"):
        j = (i.find('a'))
        j = str(j.contents[1])
        j = j.split('"')
        samples.append(j[1])
    return samples     

def songSearch(myList = []):
    b = []
    for i in myList:    
        #needs work to search multiple songs    
        a = ytm.search(query=i, filter="songs", limit=1)  
        #videoid, title, aritst name, artistid      
        b.append([a[1]['videoId'],a[1]['title'],a[1]['artists'][0]['name'],a[1]['artists'][0]['id']])        
    return b
    
def songID(mylist = []):
    a = []
    for i in mylist:
        a.append(i[0])
    return a

def playlistAdder(PID, SID):
    ytm.add_playlist_items(playlistId=PID, videoIds=SID, duplicates=False)
    return

########################

def findSongSamples(ID):    
    linkSample = samplesUrl(ID)
    samples = sampleFinder(linkSample)
    samples = songSearch(samples)
    return(samples)

def readSamples(link, samples = []):
    currentSong = ReadableData(link)
    print(f"Songs sampled in {currentSong[0]}")
    for i in samples:
        print(f"{i[1]}  {i[2]}")
    return


def main():
    linkYoutube = "https://youtu.be/Dm-foWGDBF0" #DUCKWORTH
    id = linkTOID(linkYoutube)
    samples = findSongSamples(id)
    readSamples(id, samples)

client_id = "895350166514-7ehre07r2at4tt5bb2spbsqp6a6dsb7k.apps.googleusercontent.com"
client_secret = "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"
ytm = YTMusic("oauth.json",oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))   

main()



#playlistAdder("PLv9DYoydAiAGSLnFJ1osV8qU5aVqk4XWp", samples)
#https://music.youtube.com/playlist?list=PLv9DYoydAiAGSLnFJ1osV8qU5aVqk4XWp&si=tuauDViC4-BXqheq