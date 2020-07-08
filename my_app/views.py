import requests
from django.shortcuts import render
# quote_plus automatically adds + sign between words to make them look like url
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_TESTAPPLIST_URL='https://mumbai.craigslist.org/search/jjj?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.


def home(request):
    return render(request, 'base.html')


def new_search(request):
# here we are pulling out the data using get method and as the request is POST request it is given request.POST
    search = request.POST.get('search')
# this creates an Search model object with argument as search  
    models.Search.objects.create(search=search)

    final_url=BASE_TESTAPPLIST_URL.format(quote_plus(search))
    
    response=requests.get(final_url)
# This returns the full html code of the page,so we can scrape different data from the page
    data=response.text
# this helps create the soup object
    soup=BeautifulSoup(data,features='html.parser')
  
# We can do .gethref to get the link of the class    
   
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))
        
    

    print(final_postings)

    stuff_for_frontend = {
        'search': search,
        'final_postings':final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
