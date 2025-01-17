import os

#codes of different sorter
import extension_sorter
import audio_sorter
import image_sorter
import duplicates_remover
import doc_sorter


def main(base_directory):
    # Step 1: Sort all files by extensions
    extension_sorter.sort_files(base_directory)

    # Step 2: Process audio files
    audio_directory = os.path.join(base_directory, "audio")
    if os.path.exists(audio_directory):
        audio_sorter.organize_music_in_directory(audio_directory)
    else:
        print(f"Audio directory not found: {audio_directory}")

    # Step 3: Process photos
    photos_directory = os.path.join(base_directory, "Photos")
    if os.path.exists(photos_directory):
        image_sorter.organize_by_objects(photos_directory)
    else:
        print(f"Photos directory not found: {photos_directory}")

    # Step 4: Process documents
    documents_directory = os.path.join(base_directory, "Documents")
    if os.path.exists(documents_directory):
        duplicates_remover.remove_dup(documents_directory)
        doc_sorter.sort_doc(documents_directory)
    else:
        print(f"Documents directory not found: {documents_directory}")

if __name__ == "__main__":
    # Replace this with the path of the base directory
    base_directory_path = input("Enter the path to the base directory: ").strip()
    if os.path.exists(base_directory_path):
        main(base_directory_path)
    else:
        print(f"Invalid directory path: {base_directory_path}")
