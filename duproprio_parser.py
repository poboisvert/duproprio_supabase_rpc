from supabase import create_client, Client
import os
from dotenv import load_dotenv
from utils.logger import logger
import requests
from lxml import html
import json

import os
os.chdir(os.getcwd())

PROVIDER = "DUPROPRIO"

def get_property_list_by_city():
    """ Gets a list of properties from a url """
    
    DUPROPRIO_URL = f'https://duproprio.com/en/search/list?search=true&cities%5B0%5D=1887&with_builders=1&parent=1&pageNumber=1&sort=-published_at'
    s = requests.Session()
    # Get total pages
    content = s.get(DUPROPRIO_URL).content.decode("utf-8")
    doc = html.fromstring(content)

    page_script = doc.xpath('//script/text()')
    page = next((script.split("React.createElement(window.ReactComponents.SearchPagination,")[1].split(", document.getElementById('react-component-SearchPagination'))")[0].split(',"previousLinkActive"')[0].strip() + '}' for script in page_script[20:22] if "React.createElement(window.ReactComponents.SearchPagination," in script), None)
    page_j = json.loads(page)

    print(page_j)

    total_page = len(page_j['items'])
    print('total_page: ', total_page)

    i = 0

    while (i <= total_page):
        listing = {}

        Page_URL = f'https://duproprio.com/en/search/list?search=true&cities%5B0%5D={1887}&with_builders=1&parent=1&pageNumber={3}&sort=-published_at'

        logger.info("Page_URL %s: " % Page_URL)
        content = s.get(Page_URL).content.decode("utf-8")
        doc = html.fromstring(content)

        rows = doc.xpath(
            '//ul[contains(@class, "search-results-listings-list")]//a[contains(@class, "search-results-listings-list__item-image-link ")]/@name')
        logger.info("Total Items By Page: %s" % len(rows))

        for row in rows:
            
            row = row.split("-")[1]  # listing-1047874
            # LISTING_DETAIL = f"https://duproprio.com/en/api-proxy/listing/1037778"
            LISTING_DETAIL = f"https://duproprio.com/en/api-proxy/listing/{row}"
            logger.info("listing url: " + LISTING_DETAIL)
            content = s.get(LISTING_DETAIL).json()

            listing['page_slug'] = content['address']['street']
            listing['address'] = content['address']['street']
            listing['data'] = {
                "Type": "Appartement",
                "Bedrooms": "4",
                "SizeInterior": "107.3 m2",
                "StoriesTotal": "3",
                "BathroomTotal": "2"
            }

            url: str = os.environ.get("SUPABASE_URL") or 'None'
            key: str = os.environ.get("SUPABASE_KEY") or 'None'
            supabase: Client = create_client(
                supabase_url=url, supabase_key=key)
            
            encoded_str = json.dumps(listing)
            decoded_data = json.loads(encoded_str)

            supabase.rpc('update_listing_base', listing).execute()
    



if __name__ == "__main__":
    load_dotenv()
    get_property_list_by_city()
