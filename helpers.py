#this module contains helper functions we would be calling from zincapi
import requests
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Accessing the environment variables
client_token = os.getenv('client_token')
cart=[]
contact=[]
#takes search query and searches for product
def search(query):
    response=requests.get(f'https://api.zinc.io/v1/search?query={query}&page=1&retailer=amazon',
    auth=(client_token, ''))
    result = response.json()
    return result['results']

#takes product id and stores in alist   
def add_to_cart(product):
    cart.append(product)
    print(cart)
    return cart

#take contact information
def get_contact(contact_info):
    contact.append(contact_info)
    #code that stores contact info in db
    return contact_info