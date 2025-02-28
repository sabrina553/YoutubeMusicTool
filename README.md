
# Youtube Music Tool





## Features

- Curate playlists from a song and those sampled in it.

- add/create playlists from this information

## Deployment

To deploy this project run

```bash
  git clone https://github.com/sabrina553/YoutubeMusicTool/
  cd YoutubeMusicTool/
  make
  make run
```



#### Environment Variables

To run this project, you will need the following in src/musicsampler/.env/auth/
`client_secret.json`

This has to be obtained via [google cloud console](https://console.cloud.google.com/)

- Create and navigate to a new Project, fill out any details asked

- Navigate to **API and Services**
    - Navigate to Enabled APIs and services
        - Enable API and services 
        - Search **Youtube DATA API v3** and enable
    - Navigate to Auidience
        - Add users: *Your Email*

    - Navigate to **Credentials**
        - **Create Credentials**
        - **Oauth client ID** > TV and Limited input devices
        - **Download** JSON
- Rename JSON to **client_secret.json** and move to **src/musicsampler/.env/auth/** 




## Usage/Examples
```
current usage can only be changed within the main.py main function.

User Friendlyness coming soon
```


## Documentation

[ytmusicapi: Unofficial API for YouTube Music](https://ytmusicapi.readthedocs.io/en/stable/)



## Roadmap

- convert between spotify and youtube music

- find translated covers (English -> Hindi)

- Write good code and interface authentication with apis securely and easily for new users.



## Lessons Learned

- Deployment with makefile
- Oauth
- Scraping


