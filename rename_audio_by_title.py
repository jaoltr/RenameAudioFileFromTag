import os
from mutagen import File
import sys

def sanitize_filename(name):
    """
    Replace invalid filename characters with underscores.
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

def get_unique_filename(directory, base_name, extension):
    """
    Generate a unique filename by appending a counter if a file with the same name exists.
    """
    counter = 1
    new_name = f"{base_name}{extension}"
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return new_name

def rename_audio_files(directory):
    """
    Rename all supported audio files (.mp3 and .flac) in the given directory and its subdirectories
    based on their Title tags.
    """
    supported_extensions = ['.mp3', '.flac']
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_lower = filename.lower()
            if any(file_lower.endswith(ext) for ext in supported_extensions):
                filepath = os.path.join(root, filename)  # Corrected to use 'root' instead of 'directory'
                try:
                    tags = File(filepath, easy=True)
                    if tags is None:
                        print(f"Unsupported or corrupted file '{filepath}'. Skipping.")
                        continue

                    title = tags.get('title', [None])[0]
                    if not title or title.strip() == '':
                        print(f"File '{filepath}' does not have a Title tag. Skipping.")
                        continue

                    sanitized_title = sanitize_filename(title)
                    _, ext = os.path.splitext(filename)
                    new_name = f"{sanitized_title}{ext}"
                    new_path = os.path.join(root, new_name)  # Define new_path here

                    # Check for filename conflicts and generate a unique name if necessary
                    if os.path.exists(new_path):
                        new_name = get_unique_filename(root, sanitized_title, ext)
                        new_path = os.path.join(root, new_name)

                    # Rename the file
                    os.rename(filepath, new_path)
                    print(f"Renamed '{filepath}' to '{new_path}'")

                except Exception as e:
                    print(f"Error processing '{filepath}': {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        directory = os.getcwd()
    else:
        directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"The specified directory '{directory}' does not exist or is not a directory.")
        sys.exit(1)
    
    rename_audio_files(directory)
