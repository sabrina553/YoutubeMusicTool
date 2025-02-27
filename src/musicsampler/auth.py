import os, json, sys
from ytmusicapi import YTMusic, OAuthCredentials, setup_oauth
from system import system
#from main import current_directory

def unauth():
     return YTMusic()
def get_api_key(file):
        """Retrieve the API key from the configuration file."""
        with open(file) as f:
            d = json.load(f)
            return d['installed']['client_id'], d['installed']['client_secret']

def oauth():
    #global youtube
    dir_path = system.current_directory(None)
    local_path = '/.env/auth/'
    client_secrets_file = dir_path+local_path+"YOUR_CLIENT_SECRET_FILE.json"
    oauth_file = dir_path+local_path+"oauth.json"   
    
        
    try :
        client_id, client_secret = get_api_key(client_secrets_file)
        
    except: 
        print("Client secrets file not found. \nPlease Download TV OAUTH2 Client-Secret from console.cloud.google.com and save as MusicSampler/.env/ytmapi/YOUR_CLIENT_SECRET_FILE.json")
        sys.exit(0)
        
    if not os.path.exists(oauth_file):            
        setup_oauth(client_id, client_secret,open_browser=True,filepath=oauth_file)    

    # Load credentials from the oauth_file
    return YTMusic(oauth_file, oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))