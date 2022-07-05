import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import tqdm

# python -m pip install requests beatifulsoup4 pandas tqdm

homes = []

# scraping pages 1 to 5 (non-inclusive)
for pageNumber in tqdm(range(1,5)):
    url = f'https://duproprio.com/en/search/list?search=true&is_for_sale=1&with_builders=1&parent=1&pageNumber={pageNumber}&sort=-published_at'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find_all('a', class_="search-results-listings-list__item-image-link")

    for property in content:
        title = property['title']
        url = property['href']
       
        property_info = {
            'title': title,
            'url': url
        }

        homes.append(property_info)
    
    for home in homes:
        url = home['url']
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')

        phone = soup.find('a', class_="gtm-listing-link-contact-owner-phone")['href']

        home['phone'] = phone
        
        # Sleeping 1 second between pulls
        # so that hopefully duproprio doesn't get mad :)
        time.sleep(1)
    
    print(f"Homes processed: {len(homes)}")

df = pd.DataFrame(homes)
print(df.head())

df.to_csv('homes.csv')