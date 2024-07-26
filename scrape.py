import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage to scrape
url = 'https://subdomainfinder.c99.nl/overview'  # Replace with the URL of the page you want to scrape

# Make a request to fetch the content of the page
response = requests.get(url)
if response.status_code == 200:
    page_content = response.text
else:
    print("Failed to retrieve the page.")
    exit()

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser')

# Find all <a> tags
a_tags = soup.find_all('a')

# Extract titles and format them
titles = []
for tag in a_tags:
    title = tag.get('title')
    if title:
        titles.append(title)

# Write titles to a CSV file
csv_file = 'titles.csv'  # Name of the CSV file to save
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title'])  # Write header
    for title in titles:
        writer.writerow([title])

print(f"Extracted titles have been saved to {csv_file}.")
