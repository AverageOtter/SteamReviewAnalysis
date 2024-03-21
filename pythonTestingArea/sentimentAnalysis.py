from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import torch.nn.functional as F
import torch
from collections import Counter
# Preprocess text (username and link placeholders)
def preprocess(text):
    return text

def sentimentAnal(data: list[str]) -> list:
    MODEL = "LiYuan/amazon-review-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    Sentiment = []
    star_ratings = {0: "1 star", 1: "2 stars", 2: "3 stars", 3: "4 stars", 4: "5 stars"}
    
    for rev in data:
        text = preprocess(rev)
        encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        output = model(**encoded_input)
        logits = output.logits
        probabilities = F.softmax(logits, dim=1)
        max_prob_index = torch.argmax(probabilities, dim=1)
        max_star_rating = star_ratings[max_prob_index.item()]
        Sentiment.append(max_star_rating)
    
    return Sentiment

def analytics(data):
    # Take the sentiment data, list of ['5 stars', '1 star', '5 stars']
    # Average the stars
    total_stars = 0
    num_reviews = len(data)
    star_counts = Counter(data)
    for review in data:
        star = int(review.split()[0])  # Extracting the star rating from the string
        total_stars += star

    average_stars = total_stars / num_reviews

    # Report metrics
    print("Average stars:", average_stars)
    print("Star counts:")
    for key, value in star_counts.items():
        print(f"{value} \"{key}\"")


def sentiment(data):
    sent = sentimentAnal(data)
    anal = analytics(sent)
    