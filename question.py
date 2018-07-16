from nltk import word_tokenize, pos_tag

async def analyze_question(question):
    undercase_question = question.lower()
    if "who" or "whom" in undercase_question:
        print("Person Question Detected")
    elif "which" in undercase_question:
        location_keywords = ["farthest", "closest", "furthest", "nearest"]
        location_keywords2 = ["city", "cities", "country", "countries", "building", "place", "state", "island", "location", ""]
        # if 
        