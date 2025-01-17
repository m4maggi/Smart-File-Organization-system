import PyPDF2
import hashlib
import os

def check_for_duplicates(directory):
    duplicates = []
    file_hashes = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        if file_hash in file_hashes:
            duplicates.append((file_hashes[file_hash], file_path))
        else:
            file_hashes[file_hash] = file_path

    return duplicates

def delete_duplicates(duplicates):
    for duplicate_pair in duplicates:
        print(f"Duplicate files: {duplicate_pair[0]} and {duplicate_pair[1]}")

    user_input = input("Do you want to delete the duplicate files? (yes/no): ")
    if user_input.lower() == 'yes':
        for duplicate_pair in duplicates:
            try:
                os.remove(duplicate_pair[1])
                print(f"Deleted: {duplicate_pair[1]}")
            except OSError as e:
                print(f"Error deleting {duplicate_pair[1]}: {e}")

# Example usage:
'''directory_path = 'C:/Users/megha/Desktop/del on21-11-2024'  # Current directory'''

def remove_dup(directory_path):
    duplicates = check_for_duplicates(directory_path)
    delete_duplicates(duplicates)