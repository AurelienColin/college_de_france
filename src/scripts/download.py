import os.path

from src.config import Config
from rignak.src.logging_utils import logger
from rignak.src.custom_requests.request_utils import download_file, download_from_youtube


def retry(f, *args, n: int = 5, **kwargs):
    for i in range(n):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(e)
    return


def main() -> None:
    logger("Reading pre-processed listing.")
    with open(Config.COURS_LIST_FILE, 'r') as file:
        lines = file.readlines()
    logger(f"Found {len(lines)} media.")

    i0 = i1 = 0
    to_download = {}
    previous_folder = None
    previous_subfolder = None
    for line in lines:
        try:
            folder, subfolder, timestring, basename, medial_url = line.strip().split('\t')
        except ValueError:
            logger(f"Unable to parse `{line}`")
        else:
            if folder != previous_folder:
                i0 += 1
                previous_folder = folder
            if subfolder != previous_subfolder:
                i1 += 1
                previous_subfolder = subfolder

            filename = f"{Config.DOWNLOAD_DIR}/{i0} - {folder}/{i1} - {subfolder}/{timestring} - {basename}"
            filename += ".webm" if "youtu.be" in medial_url else os.path.splitext(medial_url)[1]
            if not os.path.exists(filename):
                to_download[medial_url] = filename
    logger(f"Found {len(to_download)} media to download.")

    logger.set_iterator(len(to_download))
    for url, filename in to_download.items():
        logger(f"Attempt to download from `{url}`")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if "youtu.be" in url:
            download_from_youtube(url, filename)
        else:
            continue
            retry(download_file, url, filename)
        logger(f"\t OK -> `{filename}`")


if __name__ == "__main__":
    main()
