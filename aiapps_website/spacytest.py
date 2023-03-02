import spacy
from spacy import displacy

from CAM_NLU import Extractor


# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = ("Which drink is healthier: coffee or tea?")
doc = nlp(text)

# Analyze syntax
#print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
#print("Verbs:", [token.dep_ for token in doc ])#if token.pos_ == "NOUN"])

#print("-----")
#print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])

#doc = doc
#if " than " not in text:
#    for token in doc:
#        if token.text in (" or ", " and "):
#            obj1 = [' '.join([token.text for token in token.head.lefts if token.pos_ in ("ADJ", "ADV")]) + ' ' + token.head.text]
#            obj2 = [token.text for token in token.head.rights]
#            obj2.remove(token.text)
#            extracted_objects = obj1 + obj2
#            mod_doc = doc.text
#            for obj in extracted_objects:
#                mod_doc = mod_doc.replace(obj, "")
#            print(mod_doc)
#            asp = list(token.text for token in nlp(mod_doc) if token.pos_ in ("ADJ", "ADV"))
#else:
#    obj1 = ["dummy1"]
#    obj2 = ["dummy2"]
#    asp = ["dummy3"]

text_list = [token.lower_ for token in doc]
text_deps = [token.dep_ for token in doc]
question_starters = ["which", "how", "why", "when", "who", "where", "what"]

# CASE 1: "What is ASPECT_LIST: OBJ1 or OBJ2?"
if ":" in text_list:
    print("case1 called")
    aspect_half = text_list[:text_list.index(":")]
    object_half = text_list[text_list.index(":")+1:]
    if(len(list(set(aspect_half).intersection(question_starters))) == 0):
        aspect_half, object_half = object_half, aspect_half

    aspect_deps = [token.dep_ for token in nlp(' '.join(aspect_half))]
    aspect_text = ' '.join(aspect_half[aspect_deps.index("ROOT")+1:]).replace(" and ", ", ")
    extracted_aspects = aspect_text.split(", ")

    object_text = ' '.join(object_half).replace(" or ", ", ").replace(" and ", ", ")
    extracted_objects = object_text.split(", ")
    print(extracted_objects, extracted_aspects)

# CASE 2: "(Why/How/...) is OBJ1 ASPECT_LIST than OBJ2?"
elif "than" in text_list:
    print("case2 called")
    obj2 = ' '.join(text_list[text_list.index("than")+1:])
    aspect_deps = [token.dep_ for token in doc]
    than_head = [word for word in doc if word.lower_ == "than"][0].head
    aspect_text = [token.lower_ for token in doc if than_head in token.ancestors or than_head == token]
    extracted_aspects = ' '.join(aspect_text[:aspect_text.index("than")]).replace(" or ", ", ").replace(" and ", ", ").split(", ")
    obj1 = ' '.join(text_list[text_deps.index("ROOT")+1:text_list.index(' '.join(extracted_aspects).split()[0])])
    extracted_objects = [obj1, obj2]

# CASE 3: subcase 1 "What's the difference between OBJ1 and OBJ2?"
#         subcase 2 "(Why/How/...) Do/Are OBJ1 and OBJ2 differ/different?"
#         subcase 3 "(Why/How/...) does/is OBJ1 differ/different from OBJ2?"

elif " differ" in text:
    extracted_aspects = ["difference"]
    if("difference" in text): #subcase 1
        obj_text = text.split("between")[1]
        extracted_objects = obj_text.replace(" or ", ", ").replace(" and ", ", ").split(", ")
    elif("differ" in text_list[-1] or "differ" in text_list[-2] and "?" in text_list[-1]): #subcase 2
        obj_text = ' '.join(text_list[text_list.index([token.text for token in doc if token.pos_ in ("AUX", "VERB")][0])+1:text_list.index([token.text for token in doc if "differ" in token.text][-1])])
        extracted_objects = obj_text.replace(" and ", ", ").replace(" or ", ", ").split(", ")
    elif(" different from " in text or " differ from " in text): #subcase 3
        obj_text = ' '.join(text_list[text_list.index([token.text for token in doc if token.pos_ in ("AUX", "VERB")][0])+1:])
        if(" different from " in text):
            obj_text = obj_text.replace(" different from ", " differ from ")
        extracted_objects = obj_text.split(" differ from ")
    else: #whatever
        extracted_objects = [chunk.text for chunk in doc.noun_chunks if "differ" not in chunk]
        extracted_aspects = ["difference"]
        
# CASE 4: "(Why/how/...) Is OBJ1 or OBJ2 ASPECT_LIST?"
elif " or " in text:
    or_head = [token for token in doc if token in [t for t in doc if token.lower_ == "or"]][0].head
    right_edge_obj_text = [token for token in or_head.rights if "?" not in token.text][-1]
    if (text_list.index(right_edge_obj_text.lower_) == len(text_list)-2 and "?" in text_list[-1]) or text_list.index(right_edge_obj_text.lower_) == len(text_list)-1:
        aspect_text = text.split(or_head.text)[0].split()
        aspect_text = ' '.join(aspect_text[aspect_text.index([token.text for token in doc if token.dep_ == "ROOT"][0])+2:])
    else:
        aspect_text = text.split(right_edge_obj_text.text)[-1]
    extracted_aspects = aspect_text.replace(" and ", ", ").replace(" or ", ", ").split(", ")
    
    obj_text = text.replace(right_edge_obj_text.text, right_edge_obj_text.text+"$SPACE$").split("$SPACE$")[0]
    extracted_objects = ' '.join(obj_text.split()[obj_text.split().index([token.text for token in doc if "or" in [orhead.text for orhead in token.children]][0]):])
    extracted_objects = extracted_objects.replace(" and ", ", ").replace(" or ", ", ").split(", ")


else:
    print("caseelse called")
    extracted_objects = []
    extracted_aspects = []


print("OBJECTS RAW: ", extracted_objects)
print("ASPECTS RAW: ", extracted_aspects)

for list in [extracted_objects, extracted_aspects]:
    for element in list:
        list[list.index(element)] = list[list.index(element)].lstrip(' ') # remove leading whitespaces
        elem_proc = element.lstrip(' ')
        if "?" in elem_proc:
            list[list.index(elem_proc)] = elem_proc.replace("?","") #remove ?'s from objects if there are any ?'s

#print(displacy.render(doc, style="dep"))
#print(text_list)
print("IN SPACYTEST:")
print("OBJECTS: ", extracted_objects)
print("ASPECTS: ", extracted_aspects)

print("WITH EXTRACTOR CLASS:")
e = Extractor(text)
print(e.extract_comparative())