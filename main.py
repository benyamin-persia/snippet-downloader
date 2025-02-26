"""
main.py

Main driver script that:
  1. Prompts the user for a base name (or starting number) for the AAC files.
  2. Reads the CSV file (acclink.csv) containing PowerShell snippets in a column named "snippet".
  3. Processes each snippet by cleaning it, extracting the download URL, and parsing configuration.
  4. Sets up a requests session using the configuration from the first snippet.
  5. Downloads each file from the extracted URLs, skipping files that already exist.
"""

import os
import pandas as pd
import requests
from snippet_parser import clean_snippet, extract_url, parse_powershell_snippet, parse_additional_headers
from downloader import download_file

def main():
    # Prompt the user for the base name or starting number.
    base_input = input("Enter the base name for the AAC files (if a number, it will be incremented): ").strip()
    try:
        start_num = int(base_input)
        is_numeric = True
    except ValueError:
        is_numeric = False

    try:
        df = pd.read_csv("acclink.csv")
    except Exception as e:
        print("Failed to read acclink.csv:", e)
        return

    if "snippet" not in df.columns:
        print("Error: The CSV file must contain a column named 'snippet'.")
        return

    extracted_urls = []
    configs = []
    add_headers_list = []
    print("\nProcessing snippets from acclink.csv:")
    for index, row in df.iterrows():
        raw_snippet = str(row["snippet"])
        # Clean the snippet for consistent formatting.
        cleaned = clean_snippet(raw_snippet)
        # Extract the URL from the snippet.
        url = extract_url(cleaned)
        # Parse configuration (User-Agent and cookies) from the snippet.
        config = parse_powershell_snippet(cleaned)
        # Parse additional headers from the snippet.
        add_headers = parse_additional_headers(cleaned)
        extracted_urls.append(url)
        configs.append(config)
        add_headers_list.append(add_headers)
        # Debug output for verification.
        print(f"\nRow {index+1} original snippet:")
        print(repr(raw_snippet))
        print(f"\nRow {index+1} cleaned snippet:")
        print(repr(cleaned))
        print(f"\nRow {index+1} extracted URL: {url}")
        print(f"Row {index+1} configuration:")
        print("  User-Agent:", config.get("UserAgent"))
        if config.get("cookies"):
            for cname, cvalue in config["cookies"].items():
                print(f"  Cookie {cname}: {cvalue}")
        else:
            print("  No cookies found.")
        print(f"Row {index+1} additional headers:")
        if add_headers:
            for hkey, hvalue in add_headers.items():
                print(f"  {hkey}: {hvalue}")
        else:
            print("  No additional headers found.")

    if not any(extracted_urls):
        print("No valid URLs were extracted. Exiting.")
        return

    # Create and configure the requests session using the first snippet's data.
    session = requests.Session()
    first_config = configs[0]
    if first_config.get("UserAgent"):
        session.headers.update({"User-Agent": first_config["UserAgent"]})
    else:
        session.headers.update({
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0")
        })
    session.cookies.update(first_config.get("cookies", {}))
    first_add_headers = add_headers_list[0]
    if first_add_headers:
        session.headers.update(first_add_headers)

    # Debug: Print final session configuration.
    print("\nFinal Session Headers:")
    for key, value in session.headers.items():
        print(f"{key}: {value}")
    print("\nFinal Session Cookies:")
    for cookie in session.cookies:
        print(f"{cookie.name}: {cookie.value}")

    # Loop through the extracted URLs and download files.
    for idx, url in enumerate(extracted_urls):
        if not url:
            print(f"Row {idx+1}: No URL extracted. Skipping.")
            continue
        # Generate output filename:
        # If input is numeric, treat it as a starting number.
        if is_numeric:
            output_filename = f"{start_num + idx}.aac"
        else:
            output_filename = f"{base_input}_{idx+1}.aac"
        # Skip download if file already exists.
        if os.path.exists(output_filename):
            print(f"File '{output_filename}' already exists. Skipping download for row {idx+1}.")
            continue
        print(f"\nDownloading file {idx+1} from URL: {url}")
        download_file(session, url, output_filename)

if __name__ == "__main__":
    main()
