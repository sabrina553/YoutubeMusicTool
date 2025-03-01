#from youtube import YouTubeAPI
import whosampled
import youtube

class MusicSamplerBase:    
   
    def __init__(self):
        """Initialize the MusicSampler class."""
        self.youtube_api = youtube.YouTubeAPI()
        self.whosampled_api = whosampled.WhoSampledAPI()
        
           
    def convert_to_list(self, yay):
        """Convert a single item to a list if necessary."""
        return yay if isinstance(yay, list) else [yay]

    def flatten(self, list):
        flat_list = []
        for i in list:
            for j in i:
                flat_list.append(j)
        return flat_list
    
    def find_song_samples(self, obj_song):
        """Find samples for a list of song IDs.""" 
        samples = []              
        for song in obj_song:
            data = [song.title,  song.artist, song.videoID]
            #data = self.youtube_api.readable_data(id)   
            link_sample = self.whosampled_api.samples_url(data)            
            sample_filename = self.whosampled_api.sample_finder(link_sample)             
            sampleQuantityData = self.whosampled_api.parse_sample_main(sample_filename)   
            samplesName = self.whosampled_api.sample_main_logic(sampleQuantityData, link_sample)
            samplesName = self.flatten(samplesName)
            samples.append(self.youtube_api.song_search(samplesName))           
            
        return samples

    def read_samples(self, links, samples, link_youtube):
        """Read and print samples for a list of song links."""
        for link, sample in zip(links, samples):
            if sample:
                text = ""
                current_song = self.youtube_api.readable_data(link)
                print(f"Songs sampled in {current_song[0]} \n")
                sample_video_ids = [s[0] for s in sample]
                
                for s in sample:
                    print(f"{s[1]} - {s[2]}")
                    text += f"{s[1]} - {s[2]} \n"
                print("\n")
                # Uncomment the following line to add samples to a playlist
                self.youtube_api.add_to_playlist("https://music.youtube.com/playlist?list=PLv9DYoydAiAHE9yO_7M1hF_7G8YcgvPl-&si=vjeE5OI-n8aSzLbf", sample_video_ids)
                #self.create_playlist(link_youtube, sample_video_ids, text)

    def create_playlist(self, link_youtube, sample_video_ids, text):
         #b.append([a[0]['videoId'], a[0]['title'], a[0]['artists'][0]['name'], a[0]['artists'][0]['id']])
        #if playlist
        
        
        title = f""
        description = f""
        songs = ""        
        return youtube.create_playlist(title, description, songs)
    
    def url_To_Samples(self, link):
        self.song_objects = self.convert_to_list(self.youtube_api.link_to_id(link))  
        #print(self.song_objects)
        samples = self.find_song_samples(self.song_objects)   
        print(samples)


        #self.read_samples(ids, samples, link)
        

    def main(self):
        """Main function to find and read song samples."""    
        self.url_To_Samples("https://music.youtube.com/playlist?list=OLAK5uy_nFiS1SeXBnJII-kBfpg7kGRB0JeE_tot8")    # DAMN.
        self.url_To_Samples("https://music.youtube.com/watch?v=Dm-foWGDBF0&si=vva57r3OT6_Jdi6o")
        #self.url_To_Samples("https://music.youtube.com/watch?v=H9NuWEeODew&si=QDBiGNXdVoYTr3-N")
        
        
if __name__ == "__main__":
    sampler = MusicSamplerBase()
    sampler.main()