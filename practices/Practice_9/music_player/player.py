import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder_name):
        pygame.mixer.init()
        
        current_dir = os.path.dirname(__file__)
        self.folder = os.path.join(current_dir, music_folder_name)
        
        if not os.path.exists(self.folder):
            print(f"Error: Folder '{self.folder}' not found!")
            self.tracks = []
        else:
            self.tracks = [f for f in os.listdir(self.folder) if f.endswith('.mp3')]
            self.tracks.sort()
        
        self.current_index = 0

    def play(self):
        if self.tracks:
            track_path = os.path.join(self.folder, self.tracks[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            print(f"Now playing: {self.tracks[self.current_index]}")

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        if self.tracks:
            self.current_index = (self.current_index + 1) % len(self.tracks)
            self.play()

    def previous(self):
        if self.tracks:
            self.current_index = (self.current_index - 1) % len(self.tracks)
            self.play()