import os
from mutagen import File
import sys

def sanitize_filename(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

def rename_audio_files(directory):
    # Supported audio extensions
    supported_extensions = ['.mp3', '.flac']

    for filename in os.listdir(directory):
        file_lower = filename.lower()
        if any(file_lower.endswith(ext) for ext in supported_extensions):
            filepath = os.path.join(directory, filename)
            try:
                tags = File(filepath, easy=True)
                if tags is None:
                    print(f"Unsupported or corrupted file '{filename}'. Skipping.")
                    continue

                title = tags.get('title', [None])[0]
                if not title or title.strip() == '':
                    print(f"File '{filename}' does not have a Title tag. Skipping.")
                    continue

                sanitized_title = sanitize_filename(title)
                _, ext = os.path.splitext(filename)
                new_name = f"{sanitized_title}{ext}"
                new_path = os.path.join(directory, new_name)

                if os.path.exists(new_path):
                    print(f"Cannot rename '{filename}' to '{new_name}': target exists.")
                    continue

                os.rename(filepath, new_path)
                print(f"Renamed '{filename}' to '{new_name}'")

            except Exception as e:
                print(f"Error processing '{filename}': {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        directory = os.getcwd()
    else:
        directory = sys.argv[1]
    rename_audio_files(directory)
