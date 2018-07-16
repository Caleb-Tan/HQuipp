from nltk import pos_tag, word_tokenize
import asyncio

# special keywords
location_keywords = ["farthest", "closest", "furthest", "nearest"]
location_keywords2 = ["city", "cities", "country", "countries", "building", "place", "state", "island", "location", "area"]



def analyze_question(question, choices):
    undercase_question = question.lower()
    q_words = undercase_question.split(" ")
    word_types = pos_tag(word_tokenize(question.replace('"', "").replace("'", "").replace("following", "")))
    print(word_types)

    # deciding by question type
    if "who" in undercase_question or "whom" in undercase_question: # person question
        print("Person Question Detected")
    elif "which" in undercase_question: # multiple selection question
        extract_information("multi-selection", word_types, q_words)
        if "NOT" in q_words:
            pass
        else: 
            print("Multiple Selection Question Detected")
            if any(keyword in undercase_question for keyword in location_keywords) and any(keyword in undercase_question for keyword in location_keywords2):
                pass

def extract_information(q_type, word_types, q_words):
    subject = ""
    condition = ""

    if q_type == "multi-selection":
        if q_words.index("which") != 0: # run if part of the condition is in front of the which statement
            for i in range(0, q_words.index("which")):
                if "of" in q_words[:q_words.index("which")]:
                    if "IN" not in word_types[i][1] and "DT" not in word_types[i][1]:
                        subject += word_types[i][0] + " "
                else:
                    condition += word_types[i][0] + " "

        curr_index = q_words.index("which") + 1
        curr_type = word_types[curr_index][1]
        subject_finished = False
        subject_begun = False
        while curr_index < len(word_types)-1:
            if not subject_begun and any(grammer_type in curr_type for grammer_type in ["JJ", "NN", "CD"]):
                subject_begun = True
            if any(grammer_type in word_types[curr_index][1] for grammer_type in ["VB", "RB", "MD"]):
                subject_finished = True
            
            if not subject_finished and subject_begun:
                subject += word_types[curr_index][0] + " "
            elif subject_finished:
                condition += word_types[curr_index][0] + " "
            curr_index += 1
            curr_type = word_types[curr_index][1]
            
        print("Subject: " + subject)
        print("Condition: " + condition)





analyze_question("""Of these three British islands, which is the largest in terms of land area?""", ["Menorca", "Ibiza", "La Palma"])