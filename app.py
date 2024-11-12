import os
import pygame
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

# Initialize pygame mixer for music playback
pygame.mixer.init()

class MusicPlayerApp(App):
    def build(self):
        self.music_file = None
        
        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add music status label
        self.status_label = Label(text="No file selected", size_hint=(1, 0.2))
        layout.add_widget(self.status_label)
        
        # Add control buttons
        self.play_button = Button(text="Play", size_hint=(1, 0.2))
        self.play_button.bind(on_press=self.play_music)
        layout.add_widget(self.play_button)
        
        self.pause_button = Button(text="Pause", size_hint=(1, 0.2))
        self.pause_button.bind(on_press=self.pause_music)
        layout.add_widget(self.pause_button)
        
        self.stop_button = Button(text="Stop", size_hint=(1, 0.2))
        self.stop_button.bind(on_press=self.stop_music)
        layout.add_widget(self.stop_button)
        
        # Add file selection button
        self.choose_file_button = Button(text="Choose Audio File", size_hint=(1, 0.2))
        self.choose_file_button.bind(on_press=self.choose_file)
        layout.add_widget(self.choose_file_button)
        
        return layout

    def play_music(self, instance):
        if self.music_file:
            try:
                pygame.mixer.music.load(self.music_file)  # Load the selected music file
                pygame.mixer.music.play()  # Play the music
                self.status_label.text = f"Now Playing: {os.path.basename(self.music_file)}"
            except pygame.error as e:
                self.status_label.text = f"Error: {e}"
        else:
            self.status_label.text = "Please select an audio file!"

    def pause_music(self, instance):
        pygame.mixer.music.pause()  # Pause the music
        self.status_label.text = "Paused"

    def stop_music(self, instance):
        pygame.mixer.music.stop()  # Stop the music
        self.status_label.text = "Music Stopped"

    def choose_file(self, instance):
        # Create a file chooser
        filechooser = FileChooserIconView()
        filechooser.filters = ['*.mp3', '*.wav', '*.ogg', '*.flac']  # You can add more audio formats here
        filechooser.bind(on_selection=self.select_file)  # Bind file selection to the select_file method

        # Create a popup to display the file chooser
        popup = Popup(title="Select an Audio File", content=filechooser, size_hint=(0.8, 0.8))
        popup.open()

    def select_file(self, instance, selection):
        if selection:
            selected_file = selection[0]  # Get the selected file path
            if os.path.isfile(selected_file):
                self.music_file = selected_file  # Set the music file
                self.status_label.text = f"Selected File: {os.path.basename(self.music_file)}"
            else:
                self.status_label.text = "Invalid file selected!"

if __name__ == '__main__':
    MusicPlayerApp().run()
