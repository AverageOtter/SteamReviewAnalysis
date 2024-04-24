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

    # Convert word cloud image to Base64 encoded string
    try:
        buffer = BytesIO()
        wordcloud.to_image().save(buffer, format="PNG")
        b64_bytes = base64.b64encode(buffer.getvalue())
        b64_string = b64_bytes.decode('utf-8')
        result = b64_string
    except Exception as e:
        logger.error(f"Img to B64 Error: {e}")
        result = "ERROR"
    return result