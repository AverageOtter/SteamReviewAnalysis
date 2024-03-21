import sentimentAnalysis
import api


def main():
    game_name = input("Enter a Game Name: ")
    appid = api.get_app_id(game_name)
    resp :list = api.get_n_reviews(appid) #List of Dict
    # print(resp[0].keys
    rev = []
    for v in resp:
        rev.append(v["review"])
    results = sentimentAnalysis.sentiment(rev)
    print(results)
    
    
    
if __name__ == "__main__":
    main()