#! Generated with Gemini

import os
import internetarchive
import re
import glob
import typing
import unicodedata
import shutil

COURSES_BASE_DIR = '/media/rignak/4TO/CollègeDeFrance'
MEDIA_TYPE = 'movies'


def generate_identifier(folder_name: str):
    """
    Creates a clean, URL-friendly identifier for the Internet Archive item.
    """
    # Remove special characters, replace spaces with hyphens
    folder_name = ' - '.join(os.path.basename(folder_name).split(' - ')[1:])
    s = re.sub(r'[^\w\s-]', '', folder_name.lower())
    s = re.sub(r'[-\s]+', '-', s).strip('-_')
    s = f"CollegeDeFrance-{s}".lower()

    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s


def get_course_files(course_path: str) -> typing.List[str]:
    """
    Finds all video/audio files in a given course directory.
    """
    pattern = f"{course_path}/*/????-??-??.*"
    supported_extensions = ['.mp4', '.mov', '.avi', 'mkv', '.mp3', '.wav', '.flac', '.webm', '.m4a']
    files_to_upload = []
    for filename in glob.glob(pattern):
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            files_to_upload.append(filename)
    return files_to_upload


def get_teacher_name(folder: str) -> str:
    basename = os.path.basename(folder)
    right = basename.split(' - ')[1]
    teacher = right.split(', chaire')[0]
    return teacher


def get_title(folder: str) -> str:
    basename = os.path.basename(folder)
    left = basename.split(', chaire ')[1]

    filenames = glob.glob(f"{COURSES_BASE_DIR}/{folder}/*/????-??-??.*")
    basenames = [os.path.basename(filename) for filename in filenames]
    years = sorted((int(basename.split('-')[0]) for basename in basenames))
    return f"{left} [{years[0]}-{years[-1]}]"


def main():
    """
    Main function to iterate through directories and upload courses.
    """
    if not os.path.isdir(COURSES_BASE_DIR):
        print(f"Error: Base directory not found at '{COURSES_BASE_DIR}'")
        return

    # Get a list of all course folders
    course_folders = [d for d in os.listdir(COURSES_BASE_DIR) if os.path.isdir(os.path.join(COURSES_BASE_DIR, d))]
    total_courses = len(course_folders)
    print(f"Found {total_courses} course folders to process.")

    for i, folder_name in enumerate(course_folders):
        print("-" * 50)
        print(f"Processing course {i + 1}/{total_courses}: {folder_name}")

        # 1. Generate a unique identifier for the Internet Archive item
        identifier = generate_identifier(folder_name)
        print(f"  -> Generated Identifier: {identifier}")

        # 2. Check if this item already exists on the Internet Archive
        try:
            item = internetarchive.get_item(identifier)
            if item.exists:
                print(f"  -> SKIPPING: Item already exists at https://archive.org/details/{identifier}")
                continue
        except Exception as e:
            print(f" -> CRITICAL ERROR during item existence check for '{identifier}': {e}")

        # 3. Prepare metadata
        creator = get_teacher_name(folder_name)
        title = get_title(folder_name)

        metadata = {
            # 'collection': 'college_de_france_courses',
            'title': f"{creator} - {title}",
            'creator': creator,
            'subject': ['Collège de France', 'lecture', 'education'],
            'description': f"Courses by {creator} from chaire '{title[:-12]}', at the Collège de France.",
            'mediatype': MEDIA_TYPE,
            'publisher': 'Collège de France'
        }
        print(f"  -> Prepared metadata for title: '{metadata['title']}'")
        for key, data in metadata.items():
            print(f"\t{key}: {data}")

        # 4. Get the list of video/audio files for this course
        course_path = os.path.join(COURSES_BASE_DIR, folder_name)
        files = get_course_files(course_path)

        if not files:
            print("  -> WARNING: No media files found in this directory. Skipping.")
            continue

        print(f"  -> Found {len(files)} file(s) to upload.")

        # 5. Create a dictionary to map old filenames to new ones
        files_to_upload = {}
        for file_path in files:
            subfolder = os.path.basename(os.path.dirname(file_path))
            original_filename = os.path.basename(file_path)
            new_filename = f"{subfolder} - {original_filename}"
            files_to_upload[file_path] = new_filename

        for old, new in files_to_upload.items():
            shutil.copy(old, new)
            print(f"\t{new} \t ({old})")

        # 6. Upload the files with their new filenames
        try:
            print(f" -> Starting upload for '{identifier}'...")
            response = internetarchive.upload(identifier, files=list(files_to_upload.values()), metadata=metadata)

            # The response is a list of requests.Response objects
            if all(r.status_code == 200 for r in response):
                print(f" -> SUCCESS: Upload complete! View at: https://archive.org/details/{identifier}")
            else:
                print(f" -> ERROR: Some files may not have uploaded successfully for '{identifier}'.")
                print(f"  Response: {[r.status_code for r in response]}")

        except Exception as e:
            print(f" -> CRITICAL ERROR during upload for '{identifier}': {e}")

        for old, new in files_to_upload.items():
            os.remove(new)

if __name__ == "__main__":
    main()
