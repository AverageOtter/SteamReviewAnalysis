from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
# Preprocess text (username and link placeholders)
def preprocess(text):
    return text

def sentimentAnal(data: list[str]) -> list:
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    Sentiment = []
    for rev in data:
        text = preprocess(rev)
        encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        predicted_label_index = np.argmax(scores)  # Get the index of the label with highest probability
        predicted_label = config.id2label[predicted_label_index]  # Get the label corresponding to the index
        predicted_probability = scores[predicted_label_index]  # Get the probability of the predicted label
        Sentiment.append((predicted_label, predicted_probability, rev))  # Append review, label, and probability as a tuple to Sentiment list
    return Sentiment
    
# print(sentimentAnal(["Hello this is a house", "I hate you", "I love you"]))