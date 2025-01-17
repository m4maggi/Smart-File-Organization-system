import os
import shutil

def sort_files(directory):

 
  """Sorts files in a directory by their extension type and moves them into respective folders.

  Args:
      directory: The directory to sort.
  """

  # Create folders for different file types
  audio_dir = os.path.join(directory, 'Audio')
  video_dir = os.path.join(directory, 'Video')
  docs_dir = os.path.join(directory, 'Documents')
  pictures_dir = os.path.join(directory, 'Photos')
  codes_dir = os.path.join(directory,'Codes')
  others_dir = os.path.join(directory, 'others')
  os.makedirs(audio_dir, exist_ok=True)
  os.makedirs(video_dir, exist_ok=True)
  os.makedirs(docs_dir, exist_ok=True)
  os.makedirs(pictures_dir, exist_ok=True)
  os.makedirs(codes_dir, exist_ok=True)
  os.makedirs(others_dir, exist_ok=True)

  # Define file extensions for each category
  audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a']
  video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.wmv']
  docs_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']
  codes_extensions = [".py", ".java", ".c", ".cpp",".html"]
  pictures_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']

  # Iterate through files in the directory
  for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
      # Get file extension
      file_extension = os.path.splitext(filename)[1].lower()

      # Move file to appropriate folder
      if file_extension in audio_extensions:
        shutil.move(filepath, audio_dir)
      elif file_extension in video_extensions:
        shutil.move(filepath, video_dir)
      elif file_extension in docs_extensions:
        shutil.move(filepath, docs_dir)
      elif file_extension in pictures_extensions:
        shutil.move(filepath, pictures_dir)
      elif file_extension in codes_extensions:
        shutil.move(filepath, codes_dir)
      else:
        shutil.move(filepath, others_dir)
