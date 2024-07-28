import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL of the page to scrape
url = 'https://subdomainfinder.c99.nl/overview'  # Replace with the actual URL

# Path to the CSV file
csv_file_path = 'titles.csv'

# Time to wait between scans (in seconds)
scan_interval = 60  # Adjust as needed

def fetch_titles_from_page(url):
    try:
        # Fetch the content of the page
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all 'a' tags
        a_tags = soup.find_all('a')

        # Extract titles
        titles = set()
        for tag in a_tags:
            title = tag.get('title')
            if title:
                titles.add(title.strip())

        return titles

    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return set()

def update_csv_file(titles, csv_file_path):
    # Read existing titles from CSV file
    existing_titles = set()
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_titles = set(row[0] for row in reader)

    # Append new titles to the CSV file
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for title in titles:
            if title not in existing_titles:
                writer.writerow([title])

def main():
    while True:
        titles = fetch_titles_from_page(url)
        if titles:
            update_csv_file(titles, csv_file_path)
            print(f"Updated {csv_file_path} with new titles.")
        else:
            print("No new titles found.")
        
        print(f"Waiting {scan_interval} seconds before next scan...")
        time.sleep(scan_interval)

if __name__ == "__main__":
    main()