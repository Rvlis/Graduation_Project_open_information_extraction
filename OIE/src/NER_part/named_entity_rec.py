# import spacy

# nlp = spacy.load("en_core_web_md")


# def named_entity_rec(content):
#     doc = nlp(content)
    
#     # list_ent: text, label_, start, end
#     ent_list = list()

#     for ent in doc.ents:
#         ent_list.append([ent.text, ent.label_, ent.start, ent.end])
    
#     print(ent_list)


# named_entity_rec("Yao Ming was born in Shanghai, who is a basketball player.")

import stanza
stanza.download("en", processors="tokenize, ner")
nlp = stanza.Pipeline("en", processors="tokenize, ner")

doc = nlp("Yao Ming was born in Shanghai, which is in the east of China.")
print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in doc.ents], sep='\n')