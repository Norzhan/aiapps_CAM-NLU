import spacy
from spacy import displacy
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = ("Which is less dangerous, orange cats or dogs?")
# cheap: Apple, Android
# healthy: Cola, Pepsi
# dangerous: parachuting, diving
# difficult: german, english
# chaotic: cats, dogs
doc = nlp(text)

# Analyze syntax
#print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
#print("Verbs:", [token.dep_ for token in doc ])#if token.pos_ == "NOUN"])

#for token in doc:
#    print(token.lower_, "|", token.dep_)
print("-----")
# Find named entities, phrases and concepts
#for entity in doc.ents:
#    print(entity.text, entity.label_)
print("-----")
#print(doc.ents)
print("-----")
#print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])



# noun chunks
# 2 Objekte und 1 vergleichendes Adjektiv finden

print(displacy.render(doc, style="dep"))