import time
import json
import logging
import requests
from bs4 import BeautifulSoup

#Timing Decorator
def tictoc(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()-t1
        t2 = format(t2,'.6f')
        logging.info(f'{func.__name__} ran in {t2} seconds')
    return wrapper

#https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92 w/ editing
#! Needs NONE support, Currently Crashes if no game found
def get_app_id(game_name):
    response = requests.get(url=f'https://store.steampowered.com/search/?term={game_name}&category1=998', headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    app_id = soup.find(class_='search_result_row')['data-ds-appid']
    logging.info(f"Game {game_name} is app id {app_id}")
    return app_id

def fetch_data(*, update:bool = False, json_cache: str, url: str):
    if update:
        json_data = None
    else:
        try:
            with open(json_cache, 'r') as file:
                json_data = json.load(file)
                logging.info("GET LocalCache %s", url)
        except(FileNotFoundError, json.JSONDecodeError) as e:
            json_data = None
    if not json_data:
        json_data = requests.get(url)
        logging.info("GET Server {url} {code} {elapsed}".format(url=json_data.url, code=json_data.status_code, elapsed=json_data.elapsed))

        with open(json_cache, 'w') as file:
            json.dump(json_data.json(),file)

#https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92 w/ editing
def get_reviews(appid, params={'json':1}):
        url = 'https://store.steampowered.com/appreviews/'
        response = requests.get(url=url+appid, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        return response.json()
    
#https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92 w/ editing
def get_n_reviews(appid, n=100):
    logging.info(f"Getting {n} reviews for appid {appid}")
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

        if len(response['reviews']) < 100: break

    return reviews


@tictoc
def main():
    logging.basicConfig(filename= __file__.removesuffix(".py")+".log", format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO, )
    logging.critical("Starting Program")
    #! DEBUG TESTING
    while 1:
        match input("Enter the name of a steam game:\t").lower():
            case 'quit':
                break
            case name:
                reviews = None
                try:
                    app_id = get_app_id(name)
                    n = int(input("Enter the amount of reviews:\t"))
                    reviews = get_n_reviews(app_id, n)
                except(ValueError, TypeError) as e:
                    logging.warning(f"Tried to look up {name}, Got {e}")
                
                if reviews:
                    with open(__file__.removesuffix(".py")+".cache", 'w') as file:
                        json.dump(reviews,file)
                    print(json.dumps(reviews, indent=4))
    
    logging.critical("Ending Program")
    pass



if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as e:
        logging.exception("main crashed. Error: %s", e)