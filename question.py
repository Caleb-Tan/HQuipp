from nltk import pos_tag, word_tokenize
import asyncio
import time
import sys

sys.dont_write_bytecode = True

# special keywords
location_keywords = ["farthest", "closest", "furthest", "nearest", "located", "is in ", "is NOT in ", "found "]
location_keywords2 = ["city", "cities", "country", "countries", "territory", "territories", "building", "place", "state", "island", "mountain", "location", "area", "site", "region", "nation", "province", "district", "zone", "sector", "north", "south", "east", "west", "park"]
time_keywords = ["earliest", "most recently", "oldest", "youngest"]
base_map_url = "https://maps.googleapis.com/maps/api/staticmap?zoom=2&scale=2&size=700x500&maptype=roadmap&format=png&visual_refresh=true"

async def analyze_question(question, choices):
    start_time = time.time()
    undercase_question = question.lower().replace("whom", "who").replace(" following", "")
    q_words = undercase_question.split(" ")
    for ch in ['"', "'s", "following", "“", "”", ","]:
        question = question.replace(ch, "")
    word_types = pos_tag(word_tokenize(question))
    print(word_types)
    # deciding by question type
    if any(q_keyword in undercase_question for q_keyword in ["who", "whose"]) and not any(q_keyword in undercase_question for q_keyword in ["which", "what"]): # person question
        q_data = await extract_info_person(word_types, q_words)
        ret_data = {"type": "Character Identification", "character_type": q_data["character_type"], "condition": q_data["condition"]}
        ret_data["search_time"] = round(time.time() - start_time, 3)
        print(ret_data)
        return ret_data
    elif "which" in undercase_question: # multiple selection question
        q_data = await extract_info_multi_selection(word_types, q_words, undercase_question) # get question data (subject and condition)
        ret_data = {"type": "Multiple Selection", "subject": q_data["subject"], "condition": q_data["condition"]}
        if any(keyword in undercase_question for keyword in location_keywords) and any(keyword in undercase_question for keyword in location_keywords2): # if a map is needed  
            ret_data["type"] = "Location Identification"
            ret_data["img_url"] = await generate_map(q_data, choices)
        ret_data["search_time"] = round(time.time() - start_time, 3)
        print(ret_data)
        return ret_data
    return "x"

async def extract_info_person(word_types, q_words):
    character_type = ""
    condition = ""
    if "who" in q_words:    
        if q_words.index("who") > 1:
            lead_in = q_words[:q_words.index("who")]
            for word in lead_in:
                condition += word + " "
        condition += "<answer>" + " "
        curr_index = q_words.index("who") + 1
        curr_type = word_types[curr_index][1]
        curr_word = word_types[curr_index][0]
        character_type_reached = False
        while curr_index < len(word_types)-1:
            condition += curr_word + " "
            if not character_type_reached and curr_type in ["NN", "JJ"]: 
                character_type += curr_word + " "
            elif curr_type in ["VBZ", "VBN", "IN", "TO"] and curr_word not in ["is", "was"]:
                character_type_reached = True
            curr_index += 1
            curr_type = word_types[curr_index][1]
            curr_word = word_types[curr_index][0]
    else:
        for word in q_words:
            if word != "whose" or word != "what":
                condition += word.strip("?") + " "
    character_type = "- Implied Character -" if not character_type else character_type
    return {"character_type": character_type.rstrip(), "condition": condition.rstrip()}    
    

async def extract_info_multi_selection(word_types, q_words, undercase_question):
    subject = ""
    condition = ""
    print(word_types)
    if q_words.index("which") > 1: # run if part of the condition is in front of the which statement
        lead_in = q_words[:q_words.index("which")]
        for i in range(0, q_words.index("which")):
            curr_word = word_types[i][0]
            curr_word_text = undercase_question.split("which")[0]
            if any(keyword in curr_word_text for keyword in ["out of", "of these"]):
                if "IN" not in word_types[i][1] and "DT" not in word_types[i][1] and "CD" not in word_types[i][1]:
                    subject += curr_word + " "
            else:
                condition += curr_word + " "
    condition += "<answer>" + " "
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
        subject = "- Implied Subject -"
    
    return {"subject": subject.rstrip(), "condition": condition.rstrip()}


async def generate_map(q_data, choices):
    new_base_map_url = ""
    parameter = ""
    if q_data["subject"] != "-":
        for tag in pos_tag(word_tokenize(q_data["subject"])):
            if tag[1] in ["JJ", "NNP"]:
                parameter += "+" + tag[0]
    global base_map_url
    for i in range(0,len(choices)):
        choice = choices[i].replace(" ", "+")
        marker_link = "&markers=size:mid%7Ccolor:0xff0a00%7C" + "label:" + str(i+1) + "%7C" + choice + parameter
        new_base_map_url += base_map_url + marker_link if i == 0 else marker_link
    return new_base_map_url