# this module contains helper functions we would be calling from zincapi
import requests
import os
import requests
from decouple import config

# Accessing the environment variables
client_token = config('ZINC_API_KEY')
client_token = config('SERPAPI')

cart = []
contact=[]
# takes search query and searches for product


def amazon_search(query):
    response = requests.get(f'https://api.zinc.io/v1/search?query={query}&page=1&retailer=amazon',
                            auth=(client_token, ''))
    result = response.json()
    return result['results']

def add_to_cart(product):
    cart.append(product)
    print(cart)
    return cart

#take contact information
def get_contact(contact_info):
    contact.append(contact_info)
    #code that stores contact info in db
    return contact_info

def walmart_search(query):
    params = {
    "engine": "walmart",
    "query": {query},
    "api_key": serpapikey
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    return organic_results