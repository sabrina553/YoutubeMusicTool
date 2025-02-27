from whosampled import WhoSampledAPI
from youtube import YouTubeAPI

class MusicSampler:
    def __init__(self):
        """Initialize the MusicSampler class."""
        self.youtube_api = YouTubeAPI()
        self.whosampled_api = WhoSampledAPI()

    def convert_to_list(self, yay):
        """Convert a single item to a list if necessary."""
        return yay if isinstance(yay, list) else [yay]

    def find_song_samples(self, ids):
        """Find samples for a list of song IDs."""
        samples = []
        for id in ids:
            link_sample = self.whosampled_api.samples_url(self.youtube_api.readable_data(id))
            sample_links = self.whosampled_api.sample_finder(link_sample)
            samples.append(self.youtube_api.song_search(sample_links))
        return samples

    def read_samples(self, links, samples):
        """Read and print samples for a list of song links."""
        for link, sample in zip(links, samples):
            if sample:
                current_song = self.youtube_api.readable_data(link)
                print(f"Songs sampled in {current_song[0]} \n")
                sample_video_ids = [s[0] for s in sample]
                for s in sample:
                    print(f"{s[1]} - {s[2]}")
                print("\n")
                # Uncomment the following line to add samples to a playlist
                self.youtube_api.add_to_playlist("https://music.youtube.com/playlist?list=PLv9DYoydAiAHD85x6SP6h45MyvYeMUECF&si=mx4JLFtJ6U3t6nBw", sample_video_ids)

    def main(self):
        """Main function to find and read song samples."""
        #link_youtube = "https://music.youtube.com/playlist?list=OLAK5uy_nFiS1SeXBnJII-kBfpg7kGRB0JeE_tot8"  # DAMN.
        #ids = self.convert_to_list(self.youtube_api.link_to_id(link_youtube))
        #samples = self.find_song_samples(ids)
        #self.read_samples(ids, samples)

        cat = self.whosampled_api.sample_finder("https://www.whosampled.com/The-Notorious-B.I.G./Hypnotize/")
        print(cat)
        


if __name__ == "__main__":
    sampler = MusicSampler()
    sampler.main()