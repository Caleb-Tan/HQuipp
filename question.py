from nltk import pos_tag, word_tokenize
import asyncio

# special keywords
location_keywords = ["farthest", "closest", "furthest", "nearest"]
location_keywords2 = ["city", "cities", "country", "countries", "building", "place", "state", "island", "location", "area"]



def analyze_question(question, choices):
    undercase_question = question.lower()
    q_words = undercase_question.strip(" ")
    word_types = pos_tag(word_tokenize(question))
    print(word_types)
    # deciding by question type
    if "who" in undercase_question or "whom" in undercase_question: # person question
        print("Person Question Detected")
    elif "which" in undercase_question: # multiple selection question
        print(q_words)
        if "NOT" in q_words:
            pass
        else: 
            print("Multiple Selection Question Detected")
            extract_information("multi-selection-p", word_types, q_words)
            if any(keyword in undercase_question for keyword in location_keywords) and any(keyword in undercase_question for keyword in location_keywords2):
                pass

def extract_information(q_type, word_types, q_words):
    q_info = {"subject": "", "condition": ""}

    if q_type == "multi-selection-p":
        curr_index = q_words.find("which") + 1
        curr_type = word_types[curr_index][1]
        subject_reached = False
        while curr_index < len(word_types)-1:
            if "JJ" in curr_type or "NN" in curr_type:
                q_info["subject"] += word_types[curr_index][0] + " "
                subject_reached = True
            elif subject_reached:
                break
            curr_index += 1
            curr_type = word_types[curr_index][1]
            
        print(q_info)





analyze_question("Which food is NOT traditionally made primarily of chickpeas?", ["Menorca", "Ibiza", "La Palma"])