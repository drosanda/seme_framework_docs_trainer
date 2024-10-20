import requests
from bs4 import BeautifulSoup
import json

def extract_content(url):
    # Fetch the web page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the main content; adjust the tag and class according to your web structure
    main_content = soup.find('div', class_='main-content')  # Replace 'main-content' with the actual class or id
    
    if not main_content:
        print(f"Failed to extract content from {url}")
        return None

    # Extract text from paragraphs and code snippets
    paragraphs = [p.get_text(strip=True) for p in main_content.find_all(['p', 'li'])]
    code_snippets = [code.get_text(strip=True) for code in main_content.find_all('pre')]

    content = {
        'text': '\n'.join(paragraphs),
        'code': '\n'.join(code_snippets)
    }
    
    return content

def scrape_to_jsonl(start_url, output_file):
    # Initialize the list for storing JSONL entries
    jsonl_entries = []

    # Fetch the initial page
    content = extract_content(start_url)
    if content:
        jsonl_entries.append(content)

    # Find all links in the documentation for further scraping
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)

    base_url = 'http://localhost:3101'
    
    for link in links:
        # Get the absolute URL for each link
        href = link['href']
        if not href.startswith('http'):
            href = base_url + href

        # Extract content from each linked page
        content = extract_content(href)
        if content:
            jsonl_entries.append(content)

    # Write to a JSONL file
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in jsonl_entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

    print(f"Scraping completed. Data saved to {output_file}")

# Replace with the actual starting URL and desired output file
start_url = 'http://localhost:3101/4.0/tutorial'
output_file = 'documentation.jsonl'

scrape_to_jsonl(start_url, output_file)
