#from youtube import YouTubeAPI
import whosampled
import youtube
from multiprocessing import Process, Manager
#import os


class MusicSamplerBase:    
   
    def __init__(self):
        """Initialize the MusicSampler class."""
        self.youtube_api = youtube.YouTubeAPI()
        self.whosampled_api = whosampled.WhoSampledAPI()
        self.songs = youtube.song()
    ######################################              
    def convert_to_list(self, yay):
        """Convert a single item to a list if necessary."""
        return yay if isinstance(yay, list) else [yay]

    def flatten(self, list):
        flat_list = []
        for i in list:
            for j in i:
                flat_list.append(j)
        return flat_list
    
    def url_to_objects(self, link):
        self.song_objects = self.convert_to_list(self.youtube_api.link_to_song_object(link))          
    ######################################
    
    def find_song_samples(self):
        """Find samples for a list of song IDs."""                      
        for song in self.song_objects:  
            sample_filename = self.whosampled_api.sample_finder(song.whoSampledLink)                       
            sampleQuantityData = self.whosampled_api.parse_sample_main(sample_filename) 
            samples = self.whosampled_api.sample_main_logic(sampleQuantityData, song.whoSampledLink)            
            song.samples = self.flatten(samples)
    
    ######################################
    def samples_to_youtube(self):
        """convert found samples to youtube"""
        for i in self.song_objects:   
            for j in i.samples:                          
                self.youtube_api.song_search(j,i)
            i.samplesIDtoObject()
                  
    def read_song_objects(self):
        """read song and it's sampled"""
        for i in self.song_objects:
            i.readSamples()
            
    ######################################
    def create_playlist(self, link_youtube, sample_video_ids, text):
         #b.append([a[0]['videoId'], a[0]['title'], a[0]['artists'][0]['name'], a[0]['artists'][0]['id']])
        #if playlist        
        
        title = f""
        description = f""
        songs = ""        
        return youtube.create_playlist(title, description, songs)
      
    def main(self, url):
        """Main function to find and read song samples."""    
        #self.url_to_objects("https://music.youtube.com/watch?v=J9JFXTENxvo&si=KfXhg0q7AAuacMsa")
        self.url_to_objects(url)    # DAMN.        
        self.find_song_samples()   
        

        a = len(sampler.song_objects)
        print(a)
        ###multithread###   
        with Manager() as manager:
            processes = []
            for i in self.song_objects:
                print(i)
                process = Process(target=self._process_samples_to_youtube, args=(i,))
                processes.append(process)
                process.start()
            
            for process in processes:
                process.join()
        ###         ###
        self.read_song_objects()

    def _process_samples_to_youtube(self, song_object):
        """Helper function to process samples to YouTube in a separate thread."""
        for sample in song_object.samples:
            self.youtube_api.song_search(sample, song_object)
            song_object.samplesIDtoObject()
        
        

        

             
if __name__ == "__main__":
    sampler = MusicSamplerBase()
    url = "https://music.youtube.com/playlist?list=OLAK5uy_nFiS1SeXBnJII-kBfpg7kGRB0JeE_tot8"
    
    sampler.main(url)   