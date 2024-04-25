from .logging_config import configure_logger
import base64
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

logger = configure_logger(__name__)

def generate_wordcloud(reviews: list, path : str):
    """
    The generate_wordcloud function takes in a list of reviews and returns a dictionary containing the wordcloud image as Base64 encoded string.
    
    :param reviews: list: Pass in the list of reviews to be used for generating the wordcloud
    :return: A dictionary with the wordcloud image encoded in base64 format
    :doc-author: Trelent
    """

    reviewLength = reviews.__len__()
    if reviewLength >  0:
        logger.info(f"Generating Wordcloud of {reviewLength}")
    else:
        logger.warning(f"List Length is 0")
    combined_text = ' '.join(reviews)
    try:
        wordcloud = WordCloud(width=800, 
                          height=400, 
                          background_color='black').generate(combined_text)
    except Exception as e:
        logger.error(f"Wordcloud Generation Error: {e}")
        return None

    
    wordcloud.to_file(path)