from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
#model.save_pretrained(MODEL)
text = "After 8 years playing it, I didn't improve my skills in-game.\n\nHowever, I learned new language skills: now I can curse in Russian and Brazilian Portuguese.\n\nAlso, my tolerance level to guttural screams and loud sounds was increased.\n\nNow I can bear the crying of my children for longer and I can make them feel better by singing sweet traditional songs from other cultures, such as \u041e\u0447\u0438 \u0447\u0451\u0440\u043d\u044b\u0435 (Dark Eyes) or Garota de Ipanema (The Girl from Ipanema).\n\nIn conclusion, Counter Strike transformed me into a better father and a better person, in addition to making me more patient, tolerant to hateful people and more trained in languages and cultures.\n\nBetter than any psychiatric therapy. 10/10"
text = preprocess(text)
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
# # TF
# model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)
# model.save_pretrained(MODEL)
# text = "Covid cases are increasing fast!"
# encoded_input = tokenizer(text, return_tensors='tf')
# output = model(encoded_input)
# scores = output[0][0].numpy()
# scores = softmax(scores)
# Print labels and scores
ranking = np.argsort(scores)
ranking = ranking[::-1]
for i in range(scores.shape[0]):
    l = config.id2label[ranking[i]]
    s = scores[ranking[i]]
    print(f"{i+1}) {l} {np.round(float(s), 4)}")

