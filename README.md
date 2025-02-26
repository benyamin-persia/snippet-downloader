Below is an updated version of the README.md file with an added section that explains how to obtain a valid PowerShell snippet from the browser's Developer Tools.

---

# PowerShell Snippet Downloader

A Python application that reads PowerShell snippets from a CSV file, extracts download URLs along with session configurations (User-Agent, cookies, and headers), and downloads AAC files. The application supports automatic file naming based on a user-specified base name (or starting number) and skips files that have already been downloaded.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [File Structure](#file-structure)
- [Obtaining a Valid PowerShell Snippet](#obtaining-a-valid-powershell-snippet)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)
- [License](#license)

## Features

- **Snippet Processing:**  
  Reads a CSV file with PowerShell snippets and cleans the text for consistent parsing.

- **URL and Configuration Extraction:**  
  Extracts the download URL, User-Agent, cookies, and additional headers from each snippet.

- **Session Configuration:**  
  Sets up a Python requests session using the extracted configuration so that the HTTP request mimics the live PowerShell session.

- **Smart Downloading:**  
  Downloads AAC files using a progress bar and retries on errors. It skips files that have already been downloaded.

- **Custom File Naming:**  
  Prompts the user for a base file name. If a number is provided, it will use that as a starting point and increment it (e.g., if you enter `21`, files will be named `21.aac`, `22.aac`, etc.). If you enter a non-numeric string, it will append an underscore and an incrementing number (e.g., `myaudio_1.aac`, `myaudio_2.aac`, etc.).

## Prerequisites

- Python 3.6 or later
- pip (Python package installer)

Install the required packages by running:

```bash
pip install pandas requests tqdm
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/powershell-snippet-downloader.git
   cd powershell-snippet-downloader
   ```

2. **Install Required Packages:**

   ```bash
   pip install pandas requests tqdm
   ```

## File Structure

```
powershell-snippet-downloader/
├── acclink.csv             # CSV file containing PowerShell snippets in a column named "snippet"
├── main.py                 # Main driver script
├── snippet_parser.py       # Module for cleaning and parsing PowerShell snippets
├── downloader.py           # Module for downloading files with a progress bar and retry mechanism
└── README.md               # This file
```

## Obtaining a Valid PowerShell Snippet

To ensure the snippet you use contains valid, live authentication details, follow these steps:

1. Open your browser and navigate to the page where the audio file is being synthesized.
2. Open the Developer Tools (usually by pressing F12 or right-clicking the page and selecting "Inspect").
3. Go to the **Network** tab.
4. Wait until the synthesizing message finishes loading—look for a network request that eventually returns a status code of **200**, which indicates that the full audio file is ready.
5. Once you see the 200 status code, right-click on that network request.
6. From the context menu, select **"Copy as PowerShell"**.
7. Paste the copied snippet into your CSV file in the **snippet** column.

This method ensures that the snippet contains all the current session details (tokens, cookies, headers) required for the file download.

## Usage

1. **Prepare Your CSV File:**

   - Create or update `acclink.csv` in the project directory.
   - Ensure it contains a column named **snippet**.
   - Each row in this column should contain the complete PowerShell snippet (obtained as described above).

2. **Run the Application:**

   Open your terminal in the project directory and run:

   ```bash
   python main.py
   ```

3. **Enter the Base Name:**

   - The program will prompt:  
     `Enter the base name for the AAC files (if a number, it will be incremented):`
   - If you enter a number (e.g., `21`), the files will be named `21.aac`, `22.aac`, `23.aac`, etc.
   - If you enter a string (e.g., `myaudio`), the files will be named `myaudio_1.aac`, `myaudio_2.aac`, etc.

4. **Monitor the Process:**

   - The application processes each snippet, printing debug information (raw snippet, cleaned snippet, extracted URL, configuration, and additional headers).
   - A requests session is configured using these values.
   - Files that already exist are skipped.
   - A progress bar displays the download progress for each file.

## Troubleshooting

- **403 Forbidden Errors:**  
  If you encounter a 403 error, ensure that the tokens and cookies in your CSV snippet are fresh and valid. Use the instructions in the "Obtaining a Valid PowerShell Snippet" section to get a live snippet.

- **File Not Downloading:**  
  Verify that the CSV is formatted correctly with a column named **snippet** and that the snippet contains all the necessary details.

- **Existing Files:**  
  The app skips files that already exist. Remove or rename the existing files if you wish to re-download them.

## Customization

- **Parsing Logic:**  
  If the PowerShell snippet format changes, update the functions in `snippet_parser.py` accordingly.

- **Download Parameters:**  
  You can adjust the retry mechanism and chunk size in `downloader.py`.

- **Live Authentication:**  
  For dynamic sessions, consider integrating a live authentication flow rather than using static tokens from the CSV.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify this README.md file to better suit your project's needs.
