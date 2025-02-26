"""
snippet_parser.py

This module contains functions for processing a PowerShell snippet:
  - Cleaning the snippet text.
  - Extracting the download URL.
  - Parsing session configuration (User-Agent and cookies).
  - Parsing additional headers.
"""

import re

def clean_snippet(snippet):
    """
    Clean the raw snippet text by:
      - Replacing newline and carriage return characters with a space.
      - Collapsing multiple spaces into one.
      - Stripping leading and trailing whitespace.
    
    Args:
      snippet (str): The raw snippet text.
    
    Returns:
      str: The cleaned snippet.
    """
    cleaned = snippet.replace("\r", " ").replace("\n", " ")
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def extract_url(snippet):
    """
    Extracts the download URL from the snippet.
    
    First, it searches for a pattern like:
        -Uri "https://..."
    If not found, it falls back to finding any http(s):// URL.
    
    Args:
      snippet (str): The cleaned snippet text.
    
    Returns:
      str or None: The extracted URL, or None if not found.
    """
    pattern = r'-Uri\s+"([^"]+)"'
    match = re.search(pattern, snippet, re.IGNORECASE)
    if match:
        return match.group(1)
    url_pattern = r'(https?://[^\s"]+)'
    match = re.search(url_pattern, snippet)
    return match.group(1) if match else None

def parse_powershell_snippet(snippet):
    """
    Parses the snippet to extract session configuration.
    
    It retrieves:
      - User-Agent from a line like: $session.UserAgent = "..."
      - Cookies from lines like:
            $session.Cookies.Add((New-Object System.Net.Cookie("name", "value", "path", "domain")))
    
    Args:
      snippet (str): The cleaned snippet text.
    
    Returns:
      dict: A dictionary with keys "UserAgent" and "cookies".
    """
    config = {}
    ua_pattern = r'\$session\.UserAgent\s*=\s*"([^"]+)"'
    ua_match = re.search(ua_pattern, snippet, re.IGNORECASE)
    config["UserAgent"] = ua_match.group(1) if ua_match else None

    cookie_pattern = r'\$session\.Cookies\.Add\(\(New-Object System\.Net\.Cookie\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)\)\)'
    cookies = {}
    for name, value, path, domain in re.findall(cookie_pattern, snippet, re.IGNORECASE):
        cookies[name] = value
    config["cookies"] = cookies
    return config

def parse_additional_headers(snippet):
    """
    Extracts additional headers from the snippet.
    
    It searches for a block following "-Headers @{" and extracts key-value pairs
    in the format "key"="value".
    
    Args:
      snippet (str): The cleaned snippet text.
    
    Returns:
      dict: A dictionary of additional headers.
    """
    pattern = r'-Headers\s+@\{\s*(.*?)\s*\}'
    match = re.search(pattern, snippet, re.IGNORECASE | re.DOTALL)
    headers = {}
    if match:
        header_block = match.group(1)
        header_lines = re.findall(r'"([^"]+)"\s*=\s*"([^"]+)"', header_block)
        for key, value in header_lines:
            headers[key] = value
    return headers
