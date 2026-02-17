class Camera:
    def take_photo(self):
        print("Photo taken.")

class MusicPlayer:
    def play_music(self):
        print("Playing music.")

# Inheriting from two classes at once
class ModernPhone(Camera, MusicPlayer):
    pass

phone = ModernPhone()
phone.take_photo() # From Camera
phone.play_music() # From MusicPlayer