import os
import shutil
from mutagen import File
from mutagen.id3 import ID3NoHeaderError
import re

import os
import re
import shutil
from mutagen import File
from mutagen.id3 import ID3NoHeaderError

def sanitize_folder_name(name):
    """
    Remove or replace invalid characters in the folder name to make it valid for the filesystem.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def get_album_info(audio_file_path):
    """
    Get the album information from the audio file's metadata.
    Supports various audio formats using the mutagen File class.
    """
    try:
        audio = File(audio_file_path, easy=True)
        if audio is None:
            album = 'Unknown Album'
        else:
            album = audio.get('album', ['Unknown Album'])[0]
    except ID3NoHeaderError:
        album = 'Unknown Album'
    
    return sanitize_folder_name(album)

def organize_by_album(audio_file_path, base_directory):
    """
    Organize the audio file by album. If the album directory doesn't exist, create it.
    """
    album = get_album_info(audio_file_path)
    
    # Create the album directory if it doesn't exist
    album_directory = os.path.join(base_directory, album)
    if not os.path.exists(album_directory):
        os.makedirs(album_directory)
        print(f"Created directory: {album_directory}")
    
    # Move the audio file to the album directory
    try:
        shutil.move(audio_file_path, album_directory)
        print(f"Moved '{audio_file_path}' to '{album_directory}'")
    except Exception as e:
        print(f"Error moving file: {e}")

def organize_music_in_directory(directory):
    """
    Organize all audio files in the directory into album folders within the same directory.
    """
    supported_formats = ('.mp3', '.flac', '.aac', '.m4a', '.wav', '.ogg', '.wma')  # Add more formats as needed

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                organize_by_album(file_path, directory)

'''if __name__ == '__main__':
    # Define the directory where the audio files are located
    directory = input("Enter the path to the directory containing audio files: ").strip()
    
    if os.path.exists(directory):
        # Organize the audio files into albums
        organize_music_in_directory(directory)
    else:
        print(f"Invalid directory path: {directory}")'''

