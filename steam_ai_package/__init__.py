"""This module initializes the package and offers the client friendly function"""
from steam_ai_package import logging_config
from .api import get_app_id, get_n_reviews, get_app_details
from .artificial_intelligence import sentiment
import json

def get_sentiment_of_game(app_id):
    """
    The get_sentiment_of_game function takes in a game name 
            as a string and returns the sentiment of that game.
            The function first gets the appid of the game using get_app_id,
            then uses get_n_reviews to retrieve n reviews for that appid.
            Finally, it calls sentiment on those reviews to return an overall sentiment score.
    
    :param game: str: Specify the game that is being analyzed
    :return: The sentiment of a game
    :doc-author: Trelent
    """
    resp :list = get_n_reviews(app_id) #List of Dict
    details = get_app_details(app_id)
    rev = []
    for v in resp:
        rev.append(v["review"])
    ret = sentiment(details["name"], rev)
    ret.update(details)
    return json.dumps(ret)

def get_app_id(game_name : str):
    return api.get_app_id(game_name)