from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")


def SentimentAI(data):
    return sentiment_pipeline(data)

def main():
    data = ["I Love you", "I hate you", "This is a house", "After 8 years playing it, I didn't improve my skills in-game.\n\nHowever, I learned new language skills: now I can curse in Russian and Brazilian Portuguese.\n\nAlso, my tolerance level to guttural screams and loud sounds was increased.\n\nNow I can bear the crying of my children for longer and I can make them feel better by singing sweet traditional songs from other cultures, such as \u041e\u0447\u0438 \u0447\u0451\u0440\u043d\u044b\u0435 (Dark Eyes) or Garota de Ipanema (The Girl from Ipanema).\n\nIn conclusion, Counter Strike transformed me into a better father and a better person, in addition to making me more patient, tolerant to hateful people and more trained in languages and cultures.\n\nBetter than any psychiatric therapy. 10/10"]
    res= sentiment_pipeline(data)
    dic = {}
    for key in data:
        for value in res:
            dic[key] = value
            res.remove(value)
            break
    print(dic)

if __name__ == "__main__":
    main()
    