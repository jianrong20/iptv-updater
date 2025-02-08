import os
import requests
from datetime import datetime

def fetch_m3u(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except:
        return None

def filter_valid_entries(content):
    valid_lines = []
    lines = content.split('\n')
    for line in lines:
        if line.startswith('#EXTINF') or line.startswith('http'):
            valid_lines.append(line)
    return '\n'.join(valid_lines)

def main():
    output = ["#EXTM3U"]
    with open('sources.txt', 'r') as f:
        sources = f.read().splitlines()

    for url in sources:
        content = fetch_m3u(url)
        if content:
            filtered = filter_valid_entries(content)
            output.append(f"\n# Source: {url}\n{filtered}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output.insert(1, f"# Last Updated: {timestamp}")

    with open('jp.m3u', 'w') as f:
        f.write('\n'.join(output))

if __name__ == "__main__":
    main()
