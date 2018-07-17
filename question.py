from nltk import pos_tag, word_tokenize
import asyncio

# special keywords
location_keywords = ["farthest", "closest", "furthest", "nearest"]
location_keywords2 = ["city", "cities", "country", "countries", "building", "place", "state", "island", "location", "area", "site"]



def analyze_question(question, choices):
    undercase_question = question.lower()
    q_words = undercase_question.split(" ")
    word_types = pos_tag(word_tokenize(question.replace('"', "").replace("'s", "").replace("following", "")))
    print(word_types)

    # deciding by question type
    if any(q_keyword in undercase_question for q_keyword in ["who", "whom", "whose"]): # person question
        print("Person Question Detected")
    elif "which" in undercase_question: # multiple selection question
        print(extract_info_multi_selection(word_types, q_words))
        if "NOT" in q_words:
            pass
        else: 
            print("Multiple Selection Question Detected")
            if any(keyword in undercase_question for keyword in location_keywords) and any(keyword in undercase_question for keyword in location_keywords2):
                pass


    
def extract_info_multi_selection(word_types, q_words):
    subject = ""
    condition = ""

    if q_words.index("which") > 1: # run if part of the condition is in front of the which statement
        for i in range(0, q_words.index("which")):
            curr_word = word_types[i][0]
            if "of" in q_words[:q_words.index("which")]:
                if "IN" not in word_types[i][1] and "DT" not in word_types[i][1] and curr_word != ",":
                    subject += curr_word + " "
            else:
                if word_types[i][0] != ",":
                    condition += curr_word + " "

    curr_index = q_words.index("which") + 1
    curr_type = word_types[curr_index][1]
    curr_word = word_types[curr_index][0]
    subject_finished = False
    subject_begun = False
    while curr_index < len(word_types)-1:
        if not subject_begun and any(grammer_type in curr_type for grammer_type in ["JJ", "NN", "CD"]):
            subject_begun = True
        if any(grammer_type in curr_type for grammer_type in ["VB", "RB", "MD"]) or curr_word == "for":
            subject_finished = True
        
        if not subject_finished and subject_begun:
            if curr_word != "one":
                subject += curr_word + " "
        elif subject_finished:
            condition += curr_word + " "
        curr_index += 1
        curr_type = word_types[curr_index][1]
        curr_word = word_types[curr_index][0]
    
    if not subject:
        subject = "-"
    
    return {"subject": subject.rstrip(), "condition": condition.rstrip()}





analyze_question("""Which Texas city is farthest north?""", ["Menorca", "Ibiza", "La Palma"])