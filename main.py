import requests
import configparser
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic, OAuthCredentials

def get_api_key(id):
    config = configparser.ConfigParser()
    config.read(filenames='.env/config.ini')
    return config['oauth'][id]

def oauth():    
    global ytm
    client_id = get_api_key("client_id")
    client_secret = get_api_key("client_secret")    
    ytm = YTMusic(".env/oauth.json",oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))   
    

def init():
    oauth()
    global session
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

#https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python :)
#turn url into video ID for search Query
def linkTOID(Link):   
    query = urlparse(Link)       
    if query.hostname == 'youtu.be':
        return query.path[1:]
    
    if query.path == '/playlist': 
        return [track['videoId'] for track in ytm.get_playlist(playlistLink(Link))['tracks']]
            
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

def playlistLink(Link):               
    query = urlparse(Link)   
    return parse_qs(query.query)['list'][0]

def convertToList(yay):
    id = []
    if type(yay) != list:
        id.append(yay)
    else: 
        id = yay
    return id

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
    response = session.get(Link)      
    if response.status_code == 404:
        response = session.get(Link[:-8])

    with open('cache.html', 'wb') as f:
        f.write(response.content)
    
    samples = soup()
    return samples

def soup():
    with open('cache.html', 'rb') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')    
    samples = []   

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
        a = ytm.search(query=i, filter="songs", limit=1, ignore_spelling=True) 

        if len(a) == 1:  
            b.append([a[0]['videoId'],a[0]['title'],a[0]['artists'][0]['name'],a[0]['artists'][0]['id']])            
        elif len(a) > 1:      
            b.append([a[1]['videoId'],a[1]['title'],a[1]['artists'][0]['name'],a[1]['artists'][0]['id']])        
    return b
    
def songID(mylist = []):
    a = []
    for i in mylist:
        a.append(i[0])
    return a

def playlistAdder(PID, SID):    
    PID = playlistLink(PID)    
    ytm.add_playlist_items(playlistId=PID, videoIds=SID,duplicates=False)
    return

########################

def findSongSamples(ID):  
    a = [] 
    for i in ID:        
        linkSample = samplesUrl(i)           
        samples = sampleFinder(linkSample)              
        a.append(songSearch(samples))
       
    return(a)

def readSamples(link, samples = []):
    j=0        
    for i in link: 
        samplesVideoID = []  
        if len(samples[j]) > 0:            
            currentSong = ReadableData(i)  
            print(f"Songs sampled in {currentSong[0]} \n")  
            for k in samples[j]:  
                samplesVideoID.append(k[0])           
                print(f"{k[1]} - {k[2]}")                 
                
            print("\n")
            playlistAdder("https://music.youtube.com/playlist?list=PLv9DYoydAiAEoznKQTydhtRlKddr8Q5Zv&si=tUYoVHkAG35YnTLf", samplesVideoID)  
        j+=1
    

def main():    
    init()   
    
    linkYoutube = "https://music.youtube.com/playlist?list=OLAK5uy_mtraxOYqT3ybdDL1XzFHOXgbOH802nIkg" #DAMN.
    #linkYoutube = "https://music.youtube.com/watch?v=LfjmxgjNP2g&si=4mdjZ6LDygf9Xrsn" 
    id = linkTOID(linkYoutube)        
    id = convertToList(id)    
    samples = findSongSamples(id)     
    readSamples(id, samples)
    
main()


#1:50 for damn, 1;23 for sample bit..