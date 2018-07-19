from nltk import pos_tag, word_tokenize
import asyncio
import time
import sys

sys.dont_write_bytecode = True

# special keywords
location_keywords = ["farthest", "closest", "furthest", "nearest", "located", "is in"]
location_keywords2 = ["city", "cities", "country", "countries", "territory", "territories", "building", "place", "state", "island", "mountain", "location", "area", "site", "region", "nation", "province", "district", "zone", "sector", "north", "south", "east", "west"]
time_keywords = ["earliest", "most recently", "oldest", "youngest"]
base_map_url = "https://maps.googleapis.com/maps/api/staticmap?zoom=2&scale=2&size=700x500&maptype=roadmap&format=png&visual_refresh=true"

async def analyze_question(question, choices):
    start_time = time.time()
    undercase_question = question.lower()
    q_words = undercase_question.split(" ")
    word_types = pos_tag(word_tokenize(question.replace('"', "").replace("'s", "").replace("following", "")))
    print(word_types)

    # deciding by question type
    if any(q_keyword in undercase_question for q_keyword in ["who", "whom", "whose"]): # person question
        print("Person Question Detected")
    elif "which" in undercase_question: # multiple selection question
        q_data = await extract_info_multi_selection(word_types, q_words)
        if any(keyword in undercase_question for keyword in location_keywords) and any(keyword in undercase_question for keyword in location_keywords2): # if a map is needed
            print("Location Question Detected")
            new_base_map_url = ""
            parameter = ""
            if q_data["subject"] != "-":
                for tag in pos_tag(word_tokenize(q_data["subject"])):
                    if tag[1] in ["JJ", "NNP"]:
                            parameter += "+" + tag[0]
            global base_map_url
            for i in range(0,3):
                choice = choices[i].replace(" ", "+")
                marker_link = "&markers=size:mid%7Ccolor:0xff0a00%7C" + "label:" + str(i+1) + "%7C" + choice + parameter
                new_base_map_url += base_map_url + marker_link if i == 0 else marker_link
            
            return new_base_map_url

    
    print("--- %s seconds ---" % (time.time() - start_time))




 
async def extract_info_multi_selection(word_types, q_words):
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

