from supabase import create_client, Client
from time import sleep
from math import ceil
from random import randint
from requests import HTTPError
from datetime import datetime, date, timezone
import os
from dotenv import load_dotenv
from utils.logger import logger
import requests

import os
os.chdir(os.getcwd())

PROVIDER = "DUPROPRIO"


def get_property_list_by_city():
    """ Gets a list of properties from a url """
    listing = {}
    PAGE = 1

    DUPROPRIO_URL = f'https://duproprio.com/en/api-proxy/featured-homes?cities%5B%5D=1887&with_builders=1&parent=1&sort=-published_at&page%5Bnumber%5D={PAGE}&province=qc&page%5Bsize%5D=11&include=builders'

    try:
        req = requests.get(DUPROPRIO_URL).json()
        dataList = req['listings']

        for k, v in dataList[0].items():
            if k == 'address':
                listing['page_slug'] = v['street']
                listing['address'] = v['street']
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

        supabase.rpc('update_listing', listing).execute()
        # supabase.rpc('update_listing', {
        #              'page_slug': 'ok', 'address': '2112', 'data': '{"slug":"one"}'}).execute()
    except HTTPError:
        logger.info("Error occurred")
        sleep(randint(5, 10))


if __name__ == "__main__":
    load_dotenv()
    get_property_list_by_city()
