import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin
import time
import random
from site_finder import find_mental_health_sites

mh_resources = []

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MentalHealthResourceFinder/1.0'
}

def scrape_mental_health_site(url):
    """Scrape a single mental health resource website"""
    try:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        resource = {
            'title': extract_title(soup),
            'description': extract_description(soup),
            'contact': extract_contact(soup),
            'services': extract_services(soup),
            'source_url': url,
            'last_updated': pd.to_datetime('today').strftime('%Y-%m-%d')
        }
        
        mh_resources.append(resource)
        time.sleep(random.uniform(1, 3))  # Be polite
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")

def extract_title(soup):
    """Extract the title of the resource"""
    title = soup.find('h1')
    return title.get_text().strip() if title else "No title found"

def extract_description(soup):
    """Extract the description"""
    # Look for common description elements
    for tag in ['meta[name="description"]', 'div.description', 'div#about', 'article']:
        element = soup.select_one(tag)
        if element:
            return element.get_text().strip()[:500]  # Limit length
    
    return "No description found"

def extract_contact(soup):
    """Extract contact information"""
    # Look for phone numbers, emails, contact forms
    phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.get_text())
    email = re.search(r'[\w\.-]+@[\w\.-]+', soup.get_text())
    
    contact_info = []
    if phone: contact_info.append(f"Phone: {phone.group()}")
    if email: contact_info.append(f"Email: {email.group()}")
    
    return ", ".join(contact_info) if contact_info else "Contact info not found"

def extract_services(soup):
    """Extract services offered"""
    # Look for common service listings
    services = []
    for service in ['therapy', 'counseling', 'support', 'hotline', 'chat']:
        if service in soup.get_text().lower():
            services.append(service)
    
    return ", ".join(services) if services else "Services not specified"

def save_to_csv(filename='mental_health_resources.csv'):
    """Save scraped data to CSV"""
    df = pd.DataFrame(mh_resources)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} resources to {filename}")

SITES_TO_SCRAPE = find_mental_health_sites()

# Main scraping function
def main():
    print("Starting mental health resource scraping...")
    
    for url in SITES_TO_SCRAPE:
        scrape_mental_health_site(url)
    
    save_to_csv()
    print("Scraping complete!")

if __name__ == "__main__":
    main()