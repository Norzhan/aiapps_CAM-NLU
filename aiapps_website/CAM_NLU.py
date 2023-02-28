import spacy
from spacy import displacy
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# PATTERNS OF COMPARATIVE SENTENCES
# "(Why) Is OBJ1 ASPECT than OBJ2?"
# "Which is ASPECT: OBJ1 or OBJ2?"
# "Is OBJ1 or OBJ2 ASPECT?"
# "What's the difference between OBJ1 and OBJ2?"


#TODO Find two objects and an aspect to compare (maybe by analysing the parse tree of a comparative sentence?)
# extract objects and comparative aspect from sentence
# return list of Strings, list of Strings
def extract_comparative(input_text):
    nlp_text = nlp(input_text)

    extracted_objects = [chunk.text for chunk in nlp_text.noun_chunks]      # Most noun-chunks will be objects, most objects will be noun chunks
    extracted_pronouns = [token.text for token in nlp_text if token.pos_ == "PRON"]
    for pron in extracted_pronouns:         # Words like "Which", "Who", "What", etc. should not be considered as objects
        if pron in extracted_objects:
            extracted_objects.remove(pron)

    mod_text = input_text
    
    for noun in extracted_objects:          # Removing noun phrases removes adjectives that are not relevant for comparison
        mod_text = mod_text.replace(noun, "")
    mod_nlp_text = nlp(mod_text)
    extracted_aspects = [token.lemma_ for token in mod_nlp_text if token.pos_ == "ADJ"] # Remaining adjectives may be considered comparison aspects

    # if CCONJ "or" or "and" exists in text: 
    #    obj1 = head of CCONJ + children of obj1,
    #    obj2 = right child of head of CCONJ if child.dep_ == "conj", + children of obj2
    #    aspect = ADJ not in obj1 or obj2
    # else if ADP "than" exists in text:
    #    obj1 = 
    #    obj2 = child of "than"
    #    aspect = head of "than"

    return extracted_objects, extracted_aspects





#TODO Take extracted objects and aspects and analyse if they make a comparative sentence.
# check if extracted info forms a comparative sentence (2 objects & min. 1 aspect)
# return true if it is, else false
def check_comparative(extracted_objects, extracted_aspects):
    if(len(extracted_objects) == 2 and len(extracted_aspects) >= 1):
        return True
    return False



def main():

    #TODO Grab text input from front end
    text = "Which is less dangerous and more child-friendly: cats or dogs?" # dummy text

    # open webapp and input field
    # check if input sentence is comparative
    # e.g. "Is OBJ1 ASPECT than OBJ2?"
        # if yes, extract objects and comparative aspect
        # render selection visually in html
        # else print error message
    # send output to CAM
    extracted_info = extract_comparative(text)
    if(check_comparative(extracted_info[0], extracted_info[1])):
        output = extracted_info # 2 lists of strings
        #TODO Render selected words on webpage
        #TODO Generate CAM-URL
    
    else:
        output = "Cannot extract comparison from this sentence, please try a different sentence."
        #TODO Render error message
    print(output)

main()