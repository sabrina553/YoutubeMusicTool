# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials


def oauth():
    global youtube
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = ".env/YOUR_CLIENT_SECRET_FILE.json"
    oauth_file = ".env/oauth.json"

    # Load credentials from the oauth_file
    credentials = None
    if os.path.exists(oauth_file):
        with open(oauth_file, 'r') as token:
            credentials = Credentials.from_authorized_user_info(json.load(token), scopes)
    else:
        # If there are no (valid) credentials available, let the user log in.
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(oauth_file, 'w') as token:
            token.write(credentials.to_json())
     # Create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

def main():     
    oauth()  

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId="OLAK5uy_m_zl1RNdUJwiB2Yi1ExSwNQ0Vh3U0-LBQ"
    )

    
    tracks = request.execute()
    cat = [item['contentDetails']['videoId'] for item in tracks['items']]
    print(cat)

    """for item in tracks['items']:
        title = item['snippet']['title']
        video_id = item['contentDetails']['videoId']
        print(f"Title: {title}, Video ID: {video_id}")"""
    
    
    #return [track['videoId'] for track in self.youtube.playlistItems.list(self.playlist_link(link))['tracks']]
        
    #track = [['videoId'] for track in request.execute()]
    
    
    





if __name__ == "__main__":
    main() 