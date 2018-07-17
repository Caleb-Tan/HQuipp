from nltk import pos_tag, word_tokenize
import asyncio
import time

# special keywords
location_keywords = ["farthest", "closest", "furthest", "nearest", "located"]
location_keywords2 = ["city", "cities", "country", "countries", "territory", "territories", "building", "place", "state", "island", "mountain", "location", "area", "site", "region", "province", "district", "zone", "sector", "north", "south", "east", "west"]
time_keywords = ["earliest", "most recently", "oldest", "youngest"]
base_map_url = "https://maps.googleapis.com/maps/api/staticmap?center=krakow&zoom=1&scale=1&size=540x400&maptype=roadmap&format=png&visual_refresh=true&"

def analyze_question(question, choices):
    start_time = time.time()
    undercase_question = question.lower()
    q_words = undercase_question.split(" ")
    word_types = pos_tag(word_tokenize(question.replace('"', "").replace("'s", "").replace("following", "")))
    print(word_types)

    # deciding by question type
    if any(q_keyword in undercase_question for q_keyword in ["who", "whom", "whose"]): # person question
        print("Person Question Detected")
    elif "which" in undercase_question: # multiple selection question
        q_data = extract_info_multi_selection(word_types, q_words)
        print(q_data)
        if any(keyword in undercase_question for keyword in location_keywords) and any(keyword in undercase_question for keyword in location_keywords2):
            base_marker_url = "&markers=size:mid%7Ccolor:0xff593d%7C"
            global base_map_url
            for i in range(0,3):
                choice = choices[i]
                base_map_url += base_marker_url + "label:" + str(i+1) + "%7C" + choice
            print(base_map_url)

                
    
    print("--- %s seconds ---" % (time.time() - start_time))



    
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





analyze_question("""Which of these capital cities is in South America?""", ["Menorca", "Ibiza", "La Palma"])