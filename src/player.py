import os
import sys
import vlc
import time
import random
import logging
import subprocess
from pathlib import Path

class SlowTVPlayer:
    def __init__(self):
        # Setup paths
        self.base_dir = Path(__file__).parent.parent
        self.video_dir = self.base_dir / "videos"
        self.url_file = self.base_dir / "urls.txt"
        self.video_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.base_dir / "logs/slowtv.log")
            ]
        )
        
        # Initialize VLC
        self.instance = vlc.Instance('--fullscreen')
        self.player = self.instance.media_player_new()
        self.player.set_fullscreen(True)
        
        # Initialize state
        self.current_video = None
        self.playlist = []
        
    def download_videos(self):
        """Download videos from URLs in the url file."""
        if not self.url_file.exists():
            logging.error(f"URL file not found: {self.url_file}")
            return False
            
        with open(self.url_file) as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
        for url in urls:
            # check to see if video exists locally and log and continue if exists
            # Check if video already exists by looking for any files in video_dir
            existing_videos = list(self.video_dir.glob('*'))
            for video in existing_videos:
                if url in video.name:
                    logging.info(f"Video already exists locally: {video.name}")
                    continue
            try:
                logging.info(f"Downloading: {url}")
                subprocess.run([
                    'yt-dlp',
                    '--no-playlist',
                    '-f', 'best',
                    '-o', str(self.video_dir / '%(title)s.%(ext)s'),
                    url
                ], check=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to download {url}: {e}")
                
    def update_playlist(self):
        """Update the playlist with available video files."""
        self.playlist = [
            str(f) for f in self.video_dir.glob('*')
            if f.suffix.lower() in ('.mp4', '.mkv', '.avi', '.mov')
        ]
        
    def play_random_video(self):
        """Play a random video from the playlist."""
        if not self.playlist:
            self.update_playlist()
            if not self.playlist:
                logging.error("No videos available to play")
                return False
                
        next_video = random.choice(self.playlist)
        logging.info(f"Playing: {Path(next_video).name}")
        
        media = self.instance.media_new(next_video)
        self.player.set_media(media)
        self.player.play()
        return True
        
    def run(self):
        """Main run loop."""
        logging.info("Starting SlowTV+ player")
        self.download_videos()
        self.update_playlist()
        
        while True:
            if not self.player.is_playing():
                self.play_random_video()
            time.sleep(1)

if __name__ == "__main__":
    player = SlowTVPlayer()
    try:
        player.run()
    except KeyboardInterrupt:
        logging.info("Shutting down SlowTV+")
        sys.exit(0)