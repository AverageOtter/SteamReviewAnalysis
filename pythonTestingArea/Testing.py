import sentimentAnalysis
import api


def main():
    game_name = input("Enter a Game Name: ")
    appid = api.get_app_id(game_name)
    resp :list = api.get_n_reviews(appid) #List of Dict
    # print(resp[0].keys())
    rev = []
    for v in resp:
        rev.append(v["review"])
    sentiment = sentimentAnalysis.sentimentAnal(rev)
    # print(type(sentiment))
    
    # for index, (first, second, third) in enumerate(sentiment):
    #     # Truncate the third element to, for example, 20 characters
    #     truncated_third = third[:20] + '...' if len(third) > 20 else third
    #     print(f"Index {index}: ({first}, {second}, {truncated_third})")
    labelConfPair = [(x[0], x[1]) for x in sentiment]
    analytics(labelConfPair)
    

def analytics(labelConfPair):
        # Initialize dictionaries to store sum and count for each label
    label_confidence_sum = {"positive": 0, "neutral": 0, "negative": 0}
    label_confidence_count = {"positive": 0, "neutral": 0, "negative": 0}

    # Overall sum and count for computing overall average
    overall_sum = 0
    overall_count = 0

    # Compute sum and count for each label
    for label, confidence in labelConfPair:
        # Accumulate sum and count for each label
        label_confidence_sum[label] += confidence
        label_confidence_count[label] += 1
        
        # Accumulate overall sum and count
        overall_sum += confidence
        overall_count += 1

    # Compute average confidence for each label
    label_confidence_average = {label: label_confidence_sum[label] / label_confidence_count[label] for label in label_confidence_sum}

    # Compute overall average confidence
    overall_average = overall_sum / overall_count

    print("Average Label Confidence:")
    for label, average_confidence in label_confidence_average.items():
        print(f"{label}: {average_confidence}")

    print("Overall Average Confidence:", overall_average)
    
    
    
if __name__ == "__main__":
    main()