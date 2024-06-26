"""Holds the data processing portion using AI"""
from collections import Counter
import json
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import torch.nn.functional as F
import torch
import re
from .logging_config import configure_logger
from .wordcloud import generate_wordcloud

logger = configure_logger(__name__)

# Preprocess text (username and link placeholders)
def preprocess(text):
    """
    The preprocess function takes in a string of text and returns a list of tokens.
    The preprocess function is called by the tokenizer before it converts the text into tokens.
    This allows you to do any custom processing on your input text,
    such as lowercasing or removing punctuation.
    
    :param text: Pass the text to be preprocessed
    :return: The text after removing the stopwords and punctuations
    :doc-author: Trelent
    """
    return text

def clean_string(input_string):
    # Remove any characters that are not in the range of a-z and 0-9
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)
    return cleaned_string


def sentiment_anal(data: list[str]) -> list:
    """
    The sentiment_anal function takes in a list of strings and 
        returns the sentiment analysis for each string.
        The sentiment analysis is done by using HuggingFace's Amazon Review Sentiment Analysis model, 
        which was trained on Amazon reviews with star ratings from 1 to 5. The function first 
        preprocesses the text by removing punctuation, lowercasing all words, and removing 
        stopwords (using NLTK). Then it tokenizes the text into tokens that can be fed into the model. 
        Finally it uses HuggingFace's AutoModelForSequenceClassification class to load in
    
    :param data: list[str]: Pass in the reviews that we want to analyze
    :return: A list of tuples, where each tuple contains the sentiment analysis and text
    :doc-author: Trelent
    """
    model_name = "LiYuan/amazon-review-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    _config = AutoConfig.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_results = []
    star_ratings = {0: "1 star", 1: "2 stars", 2: "3 stars", 3: "4 stars", 4: "5 stars"}
    for rev in data:
        text = preprocess(rev)
        encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        output = model(**encoded_input)
        logits = output.logits
        probabilities = F.softmax(logits, dim=1)
        max_prob_index = torch.argmax(probabilities, dim=1)
        max_star_rating = star_ratings[max_prob_index.item()]
        sentiment_results.append((max_star_rating, text))
    return sentiment_results #returns a tuple of max star rating and text

def analytics(review_tuple, game_name):
    """
    The analytics function takes a list of strings, each string being a review.
    It then calculates the average star rating and prints out the 
    number of reviews for each star rating.
    
    
    :param review_tuple: Pass in the list of tuples
    :param game_name: Identify the game
    :return: A json object 
    :doc-author: Trelent
    """
    star_ratings = list(zip(*review_tuple))[0]
    ret = {}
    # Take the sentiment data, list of ['5 stars', '1 star', '5 stars']
    # Average the stars
    total_stars = 0
    num_reviews = len(star_ratings)
    star_counts = Counter(star_ratings)

    for review_star in star_ratings:
        star = int(review_star.split()[0])  # Extracting the star rating from the string
        total_stars += star
        

    average_stars = total_stars / num_reviews
    
    
    pos_sent_prop = ((star_counts["5 stars"] + star_counts["4 stars"])/num_reviews)*100
    neu_sent_prop = ((star_counts["3 stars"]/num_reviews)*100)
    neg_sent_prop = ((star_counts["2 stars"] + star_counts["1 star"])/num_reviews)*100
    
    
    sent_prop_data_points = [
        {"label":"Positive Sentiment", "y":pos_sent_prop},
        {"label":"Neutral Sentiment", "y":neu_sent_prop},
        {"label":"Negative Sentiment", "y":neg_sent_prop},
    ]

    sent_dist_data_points = []
    for key,value in star_counts.items():
        sent_dist_data_points.append({"label":key, "y":int((value/num_reviews)*100)})
    
    # Report metrics
    ret["star_counts"] = star_counts
    ret["avg_stars"] = round(average_stars,2)
    ret["total_stars"] = total_stars
    ret["num_reviews"] = num_reviews
    ret["sent_dist"] = sent_dist_data_points
    ret["sent_prop_dist"] = sent_prop_data_points
    
    #Generate word clouds
    posText = [] #List of text that has >=4 Stars
    NegText = [] #List of text that has <=2 Stars
    for star,text in review_tuple:
        star_int = int(star.split()[0])
        if star_int >= 4:
            posText.append(text)
        elif star_int <= 2:
            NegText.append(text)
    
    clean_game_name = clean_string(game_name)
    filepath = "/home/otter/Desktop/Capstone/SteamReviewAnalysis/core/static/Wordclouds/"
    filenamePos = clean_game_name + "Pos.png"
    filenameNeg = clean_game_name + "Neg.png"
    filePos = filepath + filenamePos
    fileNeg = filepath + filenameNeg
    generate_wordcloud(posText, filePos)
    generate_wordcloud(NegText, fileNeg)

    ret["PosWordCloud"] = "Wordclouds/" +filenamePos
    ret["NegWordCloud"] = "Wordclouds/" +filenameNeg
    return ret


def sentiment(game_name, data):
    """
    The sentiment function takes in a string of text and returns the sentiment score.
    The function uses the HuggingFace library to perform sentiment analysis 
    on the inputted text. The function then calls analytics to 
    print out results.
    
    :param game_name: Print out the game name in the log
    :param data: Pass the data to be analyzed
    :return: A tuple of the form (polarity, subjectivity)
    :doc-author: Trelent
    """
    try:
        logger.info("Calculating Sentiment for %s", game_name)
        sent = sentiment_anal(data)
        logger.info("Calculating Analytics for %s", game_name)
        ret = analytics(sent, game_name)
    except Exception as e: # pylint: disable=broad-except; Allowed for Logging purposes
        logger.exception("Sentiment crashed. Error: %s", e)
    logger.info("Finished with %s", game_name)
    return ret
