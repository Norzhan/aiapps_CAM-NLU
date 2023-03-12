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
        

    # CASE 1: "What is ASPECT_LIST: OBJ1 or OBJ2?"
    def ec_sub_case1(self): 
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
    
    # CASE 2: "(Why/How/...) is OBJ1 ASPECT_LIST than OBJ2?"
    # INTERESTING: for gerundiums: "Is GER1 ASPECT than GER2" --> ([GER2],[ASPECT])
    #         BUT: "Is ADJ1 GER1 ASPECT than ADJ GER2" --> ([ADJ1 GER1, ADJ2 GER2],[ASPECT])
    def ec_sub_case2(self): 
        obj2 = ' '.join(self.text_list[self.text_list.index("than")+1:])
        aspect_deps = [token.dep_ for token in self.doc]
        than_head = [word for word in self.doc if word.lower_ == "than"][0].head
        aspect_text = [token.lower_ for token in self.doc if than_head in token.ancestors or than_head == token]
        extracted_aspects = ' '.join(aspect_text[:aspect_text.index("than")]).replace(" or ", ", ").replace(" and ", ", ").split(", ")
        obj1 = ' '.join(self.text_list[self.text_deps.index("ROOT")+1:self.text_list.index(' '.join(extracted_aspects).split()[0])])
        extracted_objects = [obj1, obj2]
        return extracted_objects, extracted_aspects
    
    # CASE 3: subcase 1 "What's the difference between OBJ1 and OBJ2?"
    #         subcase 2 "(Why/How/...) Do/Are OBJ1 and OBJ2 differ/different?"
    #         subcase 3 "(Why/How/...) does/is OBJ1 differ/different from OBJ2?"
    def ec_sub_case3(self): 
        extracted_aspects = ["difference"]
        if("difference" in self.text): #subcase 1
            obj_text = self.text.split("between")[1]
            extracted_objects = obj_text.replace(" or ", ", ").replace(" and ", ", ").split(", ")
        elif("differ" in self.text_list[-1] or "differ" in self.text_list[-2] and "?" in self.text_list[-1]): #subcase 2
            obj_text = ' '.join(self.text_list[self.text_list.index([token.text for token in self.doc if token.pos_ in ("AUX", "VERB")][0])+1:self.text_list.index([token.text for token in self.doc if "differ" in token.text][-1])])
            extracted_objects = obj_text.replace(" and ", ", ").replace(" or ", ", ").split(", ")
        elif(" different from " in self.text or " differ from " in self.text): #subcase 3
            obj_text = ' '.join(self.text_list[self.text_list.index([token.text for token in self.doc if token.pos_ in ("AUX", "VERB")][0])+1:])
            if(" different from " in self.text):
                obj_text = obj_text.replace(" different from ", " differ from ")
            extracted_objects = obj_text.split(" differ from ")
        else: #whatever
            extracted_objects = [chunk.text for chunk in self.doc.noun_chunks if "differ" not in chunk]
            extracted_aspects = ["difference"]
        return extracted_objects, extracted_aspects
    
    # CASE 4: "(Why/how/...) Is OBJ1 or OBJ2 ASPECT_LIST?"
    def ec_sub_case4(self):
        if [token.pos_ for token in self.doc if token.dep_ == "ROOT"][0] not in ["AUX", "VERB"]:
            self.text = "What's : " + self.text
            print(self.text)
            self.doc = nlp(self.text)
            self.text_list = [token.lower_ for token in self.doc]
            self.text_deps = [token.dep_ for token in self.doc]
            return self.ec_sub_case1()
        or_token = [token for token in self.doc if token.lower_ == "or"]
        or_head = [token for token in self.doc if token.lower_ == "or"][0].head
        right_edge_obj_text = [token for token in or_head.rights if "?" not in token.text][-1]
        if (self.text_list.index(right_edge_obj_text.lower_) == len(self.text_list)-2 and "?" in self.text_list[-1]) or self.text_list.index(right_edge_obj_text.lower_) == len(self.text_list)-1:
            aspect_text = self.text.split(or_head.text)[0].split()
            aspect_text = ' '.join(aspect_text[aspect_text.index([token.text for token in self.doc if token.dep_ == "ROOT"][0])+2:])
        else:
            aspect_text = self.text.split(right_edge_obj_text.text)[-1]
        extracted_aspects = aspect_text.replace(" and ", ", ").replace(" or ", ", ").split(", ")
    
        obj_text = self.text.replace(right_edge_obj_text.text, right_edge_obj_text.text+"$SPACE$").split("$SPACE$")[0]
        extracted_objects = ' '.join(obj_text.split()[obj_text.split().index([token.text for token in self.doc if "or" in [orhead.text for orhead in token.children]][0]):])
        #extracted_objects = ' '.join(obj_text.split()[obj_text.split().index([token.lower_ for token in self.doc if token in or_head.lefts][0]):])
        extracted_objects = extracted_objects.replace(" and ", ", ").replace(" or ", ", ").split(", ")
        return extracted_objects, extracted_aspects

    def ec_sub_caseelse(self):
        nlp_text = self.doc

        extracted_objects = [chunk.text for chunk in nlp_text.noun_chunks]      # Assuming most noun-chunks will be objects, most objects will be noun chunks
        extracted_pronouns = [token.text for token in nlp_text if token.pos_ == "PRON"]
        for pron in extracted_pronouns:         # Words like "Which", "Who", "What", etc. should not be considered as objects
            if pron in extracted_objects:
                extracted_objects.remove(pron)
        #if(len(extracted_objects) != 2):        # if not exactly 2 objects have been found, return list of empty lists (no objects, no aspects)
        #    return [[],[]]

        mod_text = self.text
    
        for noun in extracted_objects:          # Removing noun phrases removes adjectives that are not relevant for comparison
            mod_text = mod_text.replace(noun, "")
        mod_nlp_text = nlp(mod_text)
        extracted_aspects = [token.text for token in mod_nlp_text if token.pos_ == "ADJ"] # Remaining adjectives may be considered comparison aspects

        return extracted_objects, extracted_aspects

    def extract_comparative(self):
        try:
            if ":" in self.text_list:
                result = self.ec_sub_case1()
            elif "than" in self.text_list:
                result = self.ec_sub_case2()
            elif " differ" in self.text:
                result = self.ec_sub_case3()
            elif " or " in self.text:
                result = self.ec_sub_case4()
            else:
                result = self.ec_sub_caseelse()
        except:
            return [[],[]]


        
        for list in result:
            for element in list:
                list[list.index(element)] = list[list.index(element)].lstrip(' ') # remove leading whitespaces
                elem_proc = element.lstrip(' ')
                if element == '':
                    list.remove('')
                if "?" in elem_proc:
                    list[list.index(elem_proc)] = elem_proc.replace("?","") #remove ?'s from objects if there are any ?'s

        return result



# check if extracted info forms a comparative sentence (2 objects & min. 1 aspect)
# return true if it is, else false
    def check_comparative(self, input_text):
        if(" or " in input_text or " than " in input_text or " and " in input_text) and len(self.extract_comparative()[0]) >= 2:
            return True
        return False



    def extracting(self):

    # open webapp and input field
    # check if input sentence is comparative
    # e.g. "Is OBJ1 ASPECT than OBJ2?"
        # if yes, extract objects and comparative aspect
        # render selection visually in html
        # else print error message
    # send output to CAM
        if(self.check_comparative(self.text)):
            extracted_info = self.extract_comparative(self.text)
            output = extracted_info # 2 lists of strings
    
        else:
            output = "Cannot extract comparison from this sentence, please try a different sentence."
        print("OUTPUT:", output)