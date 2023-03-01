import spacy
from spacy import displacy
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

class Extractor:

# PATTERNS OF COMPARATIVE SENTENCES
# "Which is ASPECT: OBJ1 or OBJ2?"
# "(Why/how/...) Is OBJ1 ASPECT than OBJ2?"
# "(Why/how/...) Is OBJ1 or OBJ2 ASPECT?"
# "What's the difference between OBJ1 and OBJ2?"

    question_starters = ["which", "how", "why", "when", "who", "where", "what"]
    def __init__(self, input_text):
        self.text = input_text
        self.doc = nlp(self.text)
        self.text_list = [token.lower_ for token in self.doc]
        self.text_deps = [token.dep_ for token in self.doc]

#TODO Find two objects and an aspect to compare (maybe by analysing the parse tree of a comparative sentence?)
# extract objects and comparative aspect from sentence
# return list of Strings, list of Strings
    def ec_sub_case1(self, input_text):
        aspect_half = self.text_list[:self.text_list.index(":")]
        object_half = self.text_list[self.text_list.index(":")+1:]
        if(len(list(set(aspect_half).intersection(self.question_starters))) == 0):
            aspect_half, object_half = object_half, aspect_half

        aspect_deps = [token.dep_ for token in nlp(' '.join(aspect_half))]
        aspect_text = ' '.join(aspect_half[aspect_deps.index("ROOT")+1:]).replace(" and ", ", ")
        extracted_aspects = aspect_text.split(", ")

        object_text = ' '.join(object_half).replace(" or ", ", ").replace(" and ", ", ")
        extracted_objects = object_text.split(", ")
        return extracted_objects, extracted_aspects
    
    def ec_sub_case2(self, input_text):
        obj2 = ' '.join(self.text_list[self.text_list.index("than")+1:])
        aspect_deps = [token.dep_ for token in self.doc]
        than_head = [word for word in self.doc if word.lower_ == "than"][0].head
        aspect_text = [token.lower_ for token in self.doc if than_head in token.ancestors or than_head == token]
        extracted_aspects = ' '.join(aspect_text[:aspect_text.index("than")]).replace(" or ", ", ").replace(" and ", ", ").split(", ")
        obj1 = ' '.join(self.text_list[self.text_deps.index("ROOT")+1:self.text_list.index(' '.join(extracted_aspects).split()[0])])
        extracted_objects = [obj1, obj2]
        return extracted_objects, extracted_aspects
    
    def ec_sub_case3(self, input_text):
        extracted_objects = []
        extracted_aspects = []
        return extracted_objects, extracted_aspects
    
    def ec_sub_case4(self, input_text):
        extracted_objects = []
        extracted_aspects = []
        return extracted_objects, extracted_aspects

    def ec_sub_caseelse(self,input_text):
        nlp_text = nlp(input_text)

        extracted_objects = [chunk.text for chunk in nlp_text.noun_chunks]      # Assuming most noun-chunks will be objects, most objects will be noun chunks
        extracted_pronouns = [token.text for token in nlp_text if token.pos_ == "PRON"]
        for pron in extracted_pronouns:         # Words like "Which", "Who", "What", etc. should not be considered as objects
            if pron in extracted_objects:
                extracted_objects.remove(pron)
        if(len(extracted_objects) != 2):        # if not exactly 2 objects have been found, return list of empty lists (no objects, no aspects)
            return [[],[]]

        mod_text = input_text
    
        for noun in extracted_objects:          # Removing noun phrases removes adjectives that are not relevant for comparison
            mod_text = mod_text.replace(noun, "")
        mod_nlp_text = nlp(mod_text)
        extracted_aspects = [token.lemma_ for token in mod_nlp_text if token.pos_ == "ADJ"] # Remaining adjectives may be considered comparison aspects

        return extracted_objects, extracted_aspects

    def extract_comparative(self, input_text):
        if ":" in self.text_list:
            return self.ec_sub_case1(input_text)
        elif "than" in self.text_list:
            return self.ec_sub_case2(input_text)
        else:
            return self.ec_sub_caseelse(input_text)



#TODO Take extracted objects and aspects and analyse if they make a comparative sentence.
# check if extracted info forms a comparative sentence (2 objects & min. 1 aspect)
# return true if it is, else false
    def check_comparative(self, input_text):
        if(" or " in input_text or " than " in input_text or " and " in input_text):
            return True
        return False



    def extracting(self):

    #TODO Grab text input from front end
        text = "Which is less dangerous and more child-friendly: cats or dogs?" # dummy text

    # open webapp and input field
    # check if input sentence is comparative
    # e.g. "Is OBJ1 ASPECT than OBJ2?"
        # if yes, extract objects and comparative aspect
        # render selection visually in html
        # else print error message
    # send output to CAM
        if(self.check_comparative(text)):
            extracted_info = self.extract_comparative(text)
            output = extracted_info # 2 lists of strings
        #TODO Render selected words on webpage
        #TODO Generate CAM-URL
    
        else:
            output = "Cannot extract comparison from this sentence, please try a different sentence."
        #TODO Render error message
        print(output)