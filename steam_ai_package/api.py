"""
This module handles grabbing reviews from the Steam API
"""
# import logging
import requests
from bs4 import BeautifulSoup
from .logging_config import configure_logger

logger = configure_logger(__name__)

#! Needs NONE support, Currently Crashes if no game found & if timeout

#https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92 w/ editing
def get_app_id(game_name):
    """
    The get_app_id function takes a game name and returns the app id of that game.
    
    :param game_name: Search for the game on steam
    :return: The app_id of the game
    :doc-author: Trelent
    """
    response = requests.get(
        url=f'https://store.steampowered.com/search/?term={game_name}&category1=998',
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    app_id = soup.find(class_='search_result_row')['data-ds-appid']
    logger.info("Game %s is app id %s", game_name, app_id)
    return app_id

#https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92 w/ editing
def get_reviews(appid, params=None):
    """
    The get_reviews function takes an appid and a dictionary of parameters as input.
    The function then makes a request to the Steam store for reviews of the given appid,
    using the provided parameters. The function returns a JSON object containing all 
    reviews that match the given criteria.
    
    :param appid: Specify which app's reviews we want to get
    :param params: Specify the parameters in the url
    :return: A dictionary
    :doc-author: Trelent
    """
    if params is None:
        params = {'json': 1}
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url+appid, params=params,
                            headers={'User-Agent': 'Mozilla/5.0'},
                            timeout=10)
    return response.json()

#https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92 w/ editing
def get_n_reviews(appid, n=100):
    """
    The get_n_reviews function takes in an appid and a number of reviews to return.
    It then returns the specified number of reviews for that appid.
    
    
    :param appid: Specify which game's reviews to get
    :param n: Specify how many reviews you want to get
    :return: A list of reviews
    :doc-author: Trelent
    """
    logger.info("Getting %d reviews for appid %s", n, appid)
    reviews = []
    cursor = '*'
    params = {
            'json' : 1,
            'filter' : 'all',
            'language' : 'english',
            'day_range' : 9223372036854775807,
            'review_type' : 'all',
            'purchase_type' : 'all'
            }

    while n > 0:
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)
        n -= 100

        response = get_reviews(appid, params)
        cursor = response['cursor']
        reviews += response['reviews']
        if len(response['reviews']) < 100:
            break
    return reviews
