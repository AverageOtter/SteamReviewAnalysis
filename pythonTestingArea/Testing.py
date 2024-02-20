import sentimentAnalysis
import api


def main():
    game_name = input("Enter a Game Name: ")
    appid = api.get_app_id(game_name)
    resp :list = api.get_n_reviews(appid) #List of Dict
    print(resp[0].keys())
    rev = []
    for v in resp:
        rev.append(v["review"])
    sentiment = sentimentAnalysis.sentiment_pipeline(rev)
    print(type(sentiment))
    

if __name__ == "__main__":
    main()