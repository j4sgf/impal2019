import csv
import spacy

en_nlp = spacy.load('en_core_web_sm')

text = ("At 12:05 a.m., a Burlington police officer saw people in three different vehicles on Piedmont Way near Mebane Street chasing and shooting at each other from inside the moving vehicles, according to a police news release. Officers stopped one of the vehicles, a tan 2001 Chevrolet Tahoe, at the intersection of North Mebane Street and Webb Avenue. Officers found a stolen handgun and controlled substances.")
print(text)
doc = en_nlp(text)

for entity in doc.ents:
    print(entity.text, entity.label_)

doc1 = en_nlp(u"my fries were super gross")
doc2 = en_nlp(u"such disgusting fries")
similarity = doc1.similarity(doc2)
print(doc1.text, doc2.text, similarity)
