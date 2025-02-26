"""
downloader.py

This module provides the download_file function which uses a requests session
to download a file from a URL, using streaming and a progress bar. It retries
on errors.
"""

import os
import time
import requests
from tqdm import tqdm

def download_file(session, url, filename, chunk_size=8192, retry_delay=1, timeout=(10, 60)):
    """
    Downloads the file from the given URL using the provided requests session.
    
    The function streams the file in chunks and writes it to 'filename'. A
    progress bar displays the download progress. If any error occurs, it waits
    for a specified delay before retrying.
    
    Args:
      session (requests.Session): The configured session.
      url (str): The URL to download from.
      filename (str): The output filename.
      chunk_size (int): The size of each chunk to read.
      retry_delay (int): Seconds to wait before retrying on error.
      timeout (tuple): Connection and read timeouts.
    """
    while True:
        try:
            print(f"\nAttempting to download: {url}")
            response = session.get(url, stream=True, timeout=timeout)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()  # Raises HTTPError for bad responses.
            total_size = int(response.headers.get("content-length", 0))
            with open(filename, "wb") as f, tqdm(total=total_size, unit="B", unit_scale=True,
                                                  desc=f"Downloading {filename}") as progress:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        progress.update(len(chunk))
            print(f"Download complete. File saved as {filename}\n")
            break  # Exit loop if download is successful.
        except Exception as e:
            print(f"Error encountered: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
