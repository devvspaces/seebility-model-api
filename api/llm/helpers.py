# this module contains helper functions we would be calling from zincapi
import requests
import os
import requests
from decouple import config

# Accessing the environment variables
client_token = config('ZINC_API_KEY')
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