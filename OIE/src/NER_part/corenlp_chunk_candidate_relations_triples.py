"""
Extracting Relation Triples"
"""
import sys
sys.path.append(".")

from stanza.server import CoreNLPClient
import os
from tqdm import tqdm
import scenarios        # implementation of 6 scenarios
# import pre_process_text # implementation of preprocess text
# from scripts import myutils
import coref
import spacy
nlp = spacy.load("en_core_web_md")
import csv

# Table Ⅰ. REGULAR EXPRESSION OF DIFFERENT CHUNKS
VVP_pattern = [
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(TO*)+(VB)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:TO]{1,})([pos:VB]{1,})",
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:IN]{1,})([pos:VBG]{1,})",
    # new: was a large and densely populated island in
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:JJ]*)([pos:CC]?)([pos:RB]*)([pos:/VB.*/]*)([pos:/NN.*/]*)([pos:/IN|TO/]{1,})",
]

VP_pattern = [
    # (MD)*(VB.*)+(CD)*(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:CD]*)([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:/IN|TO/]{1,})",
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
    # "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:/IN|TO/]{1,})",
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]{1,})",
    
    # (MD)*(VB.*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})",

    # new: is in the east of
    "([pos:/VB.*/]{1,})([pos:/IN|TO/]{1,})([pos:DT]?)([pos:/NN.*/]*)([pos:/IN|TO/]{1,})",
    "([pos:/VB.*/]{1,})([pos:DT]?)([pos:/NN.*/]*)([pos:/IN|TO/]{1,})",
    # apposition
    "([pos:DT]?)([pos:JJ]*)([pos:/NN.*/]{1,})([pos:/IN|TO/]{1,})",

    "([pos:/VB.*/]{1,})([pos:RB]*)([pos:/VB.*/]{1,})([pos:RB]*)([pos:/IN|TO/]{1,})"
]

NP_pattern = [
    # "([pos:IN]{1,}[his][pos:NN]{1,})",
    # (CD)*(DT)?(CD)*(JJ)*(CD)*(VBD|VBG)*(NN.*)*-
    # (POS)*(CD)*(VBD|VBG)*(NN.*)*-
    # (VBD|VBG)*(NN.*)*(POS)*(CD)*(NN.*)+
    # "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})",    
    "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:RB]*)([pos:HYPH]?)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})",
    "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:RB]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})",
    # "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})",
    # "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})([pos:CC]?)([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})",
    "([pos:PRP]{1,})",
    "([pos:RB]*)([pos:JJ]*)"
]

def in_conj_and(np, source):
    if source >= np[1] and source < np[2]:
        return True
    return False
def in_amod(np, source):
    if source >= np[1] and source < np[2]:
        return True
    return False

def NP_extension_1(input_sentence, tokens, dependency_rel, NPs):
    """
    adjective modifier fine-grained
    :param input_sentence: str
    :param tokens: list, [token.word, token.beginChar, token.endChar, token.tokenBeginIndex, token.tokenEndIndex, token.pos]
    :param dependency_rel: list, [source_index, target_index, dependency] 
    :param NPs: list, [text, start, end]

    :return extended_NPs: list, [text, start, end]
    """

    extended_NPs = list()

    conj_and = [item for item in dependency_rel if "conj:and" in item[2] or "conj:or" in item[2]]
    amod = [item for item in dependency_rel if "amod" in item[2]]
    # print("conj_and:", conj_and)
    # print("amod:", amod)
    for c_item in conj_and:
        c_source = c_item[0]
        c_target = c_item[1]
        for np in NPs:
            if in_conj_and(np, c_source) and not in_conj_and(np, c_target):
                for a_item in amod:
                    a_source = a_item[0]
                    a_target = a_item[1]
                    root = a_source
                    if in_amod(np, a_target) and a_target == c_source:
                        for aa_item in amod:
                            aa_source = aa_item[0]
                            aa_target = aa_item[1]
                            if aa_source == a_source and aa_target == a_target:
                                continue
                            if not in_amod(np, aa_target) and aa_target == c_target and aa_source == root:
                                extended_NPs.append([str(tokens[aa_target][0]) + " " + str(tokens[root][1]), root, root+1])


            elif in_conj_and(np, c_target) and not in_conj_and(np, c_source):
                for a_item in amod:
                    a_source = a_item[0]
                    a_target = a_item[1]
                    root = a_source
                    if in_amod(np, a_target) and a_target == c_target:
                        for aa_item in amod:
                            aa_source = aa_item[0]
                            aa_target = aa_item[1]
                            if aa_source == a_source and aa_target == a_target:
                                continue
                            if not in_amod(np, aa_target) and aa_target == c_source and aa_source == root:
                                extended_NPs.append([str(tokens[aa_target][0]) + " " + str(tokens[root][0]), root, root+1])

    return extended_NPs

def NP_extension_2(input_sentence, tokens, dependency_rel, NPs):
    """
    noun modifier fine-grained
    :param input_sentence: str
    :param tokens: list, [token.word, token.beginChar, token.endChar, token.tokenBeginIndex, token.tokenEndIndex, token.pos]
    :param dependency_rel: list, [source_index, target_index, dependency] 
    :param NPs: list, [text, start, end]

    :return extended_NPs: list, [text, start, end]
    """
    extended_NPs = list()

    conj_and = [item for item in dependency_rel if "conj:and" in item[2]]
    for c_item in conj_and:
        c_source = c_item[0]
        c_target = c_item[1]
        for np_1 in NPs:
            if in_conj_and(np_1, c_source) and tokens[c_source][5] == "NN":
                for np_2 in NPs:
                    if np_1[1] == np_2[1] and np_1[2] == np_2[2]:
                        continue 
                    if in_conj_and(np_2, c_target) and tokens[c_target][5] == "NN":
                        # root = c_target
                        source_noun = tokens[c_source][0]
                        target_noun = tokens[c_target][0]
                        end = np_1[0].find(source_noun)
                        if end != -1 and end != 0:
                            adj_modifier = np_1[0][:end]
                            extended_NPs.append([adj_modifier + target_noun, c_target, c_target+1])
    return extended_NPs


def remove_overlap(NPs, extended_NPs):
    """
    remove overlapped np in NPs and extended NPs
    :param NPs: list, [text, start, end]
    :param extended_NPs: list, [text, start, end]
    :return NPs: list, NPs with non-overlapped np
    """
    for e_np in extended_NPs:
        e_text = e_np[0]
        flag = True
        for np in NPs:
            text = np[0]
            if e_text in text:
                flag = False
                break
            if text in e_text:
                NPs.remove(np)
        if flag:
            NPs.append(e_np)
    return NPs


def chunk_candidate_relation_triples(input_sentences):
    """
    :param input_sentences: list[[sent_id1, raw_sentence1, simplified_sentence1], [sent_id1, raw_sentence1, simplified_sentence2], ..., [sent_id2, raw_sentence2, simplified_sentence1]]
    :return candidate_relation_triples: list[[raw_sentence1, verb_phrase, arg1, arg2], [raw_sentence1, verb_phrase, arg1, arg2], ..., [raw_sentence2, verb_phrase, arg1, arg2] ]
    """
    candidate_relation_triples = list()
    # set up the client
    with CoreNLPClient(annotators=['tokenize','ssplit','pos','depparse'], timeout=60000, memory='4G', be_quiet=True) as client:
        print("-------------------- Extracting Relation Triples --------------------")
        sce_dist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for item in tqdm(input_sentences):
            sent_id = item[0]
            raw_sentence = item[1]
            input_sentence = item[2]
            # print(input_sentence)
            # os.system("pause")
            # print("input_sentence:", input_sentence)
            ann = client.annotate(input_sentence)
            

            # sentence = ann.sentence[0]
            for sentence_index in range(len(ann.sentence)):
                sentence = ann.sentence[sentence_index]
                # print("sentence:", sentence)
                annotated_tokens = list(sentence.token)
                
                tokens = list()
                for token in annotated_tokens:
                    tokens.append([token.word, token.beginChar, token.endChar, token.tokenBeginIndex, token.tokenEndIndex, token.pos])
                # print(tokens)
                # print("sentence:", sentence)
                # print("tokenize:",sentence[10])

                # HDSKG's method
                # denpendency_rel: source, target, dep
                dependency_rel = list()
                enhanced_plus_plus_dependency_parse = sentence.enhancedPlusPlusDependencies
                edges = list(enhanced_plus_plus_dependency_parse.edge)
                for edge in edges:
                    # print(type(edge.source),type(edge.target),type(edge.dep))
                    dependency_rel.append([edge.source-1, edge.target-1, edge.dep])
                # print(list(enhanced_plus_plus_dependency_parse.edge))
                # for item in dependency_rel:
                #     print(item)
                # os.system("pause")
                VPs = list()
                NPs = list()
                

                # VVP_pattern
                p_index = 0
                pattern_list = list()
                for pattern in VVP_pattern:
                    p_index += 1
                    matches = client.tokensregex(input_sentence, pattern)
                    # length means the number of matched phrase
                    length = matches["sentences"][sentence_index]["length"]
                    if length != 0:
                        for i in range(length):
                            text = matches["sentences"][sentence_index][str(i)]["text"]
                            begin = matches["sentences"][sentence_index][str(i)]["begin"]
                            end = matches["sentences"][sentence_index][str(i)]["end"]
                            # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                            flag = True
                            for item in VPs:
                                if begin >= item[1] and end <= item[2]:
                                    flag = False
                                    break
                                if begin <= item[1] and end >= item[2]:
                                    VPs.remove(item)
                            if flag:
                                pattern_list.append(["VVP", p_index, text])
                                VPs.append([text,begin,end])
                            # VPs.append([text,begin,end])

                # VP_pattern
                p_index = 0
                for pattern in VP_pattern: 
                    p_index += 1
                    matches = client.tokensregex(input_sentence, pattern)
                    # print(matches)
                    # length means the number of matched phrase
                    length = matches["sentences"][sentence_index]["length"]
                    if length != 0:
                        for i in range(length):
                            text = matches["sentences"][sentence_index][str(i)]["text"]
                            
                            begin = matches["sentences"][sentence_index][str(i)]["begin"]
                            end = matches["sentences"][sentence_index][str(i)]["end"]
                            # print("text:", text)
                            # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                            # VP存在重复匹配问题，需要多加一步判断
                            flag = True
                            for item in VPs:
                                if begin >= item[1] and end <= item[2]:
                                    flag = False
                                    break
                                if begin <= item[1] and end >= item[2]:
                                    VPs.remove(item)
                            if flag:
                                VPs.append([text,begin,end])
                                pattern_list.append(["VP", p_index, text])
                    



                # NP_pattern
                # Spacy NER
                NP_set = set()
                doc = nlp(input_sentence)
                for ent in doc.ents:
                    # print("ent:", ent)
                    flag = True
                    # if VP contains NP, remove this NP
                    for vp_item in VPs:
                        if ent.start >= vp_item[1] and ent.end <= vp_item[2]:
                            flag = False
                            break
                    # if flag == True and ent.text not in NP_set:
                    #     NP_set.add(ent.text)
                    #     NPs.append([ent.text, ent.start, ent.end])
                    if flag == True:
                        # NP_set.add(ent.text)
                        NPs.append([ent.text, ent.start, ent.end])
                # rule-based NER
                p_index = 0
                for pattern in NP_pattern:
                    p_index += 1
                    matches = client.tokensregex(input_sentence, pattern)
                    # print(matches)
                    # length means the number of matched phrase
                    length = matches["sentences"][sentence_index]["length"]
                    if length != 0:
                        for i in range(length):
                            text = matches["sentences"][sentence_index][str(i)]["text"]
                            begin = matches["sentences"][sentence_index][str(i)]["begin"]
                            end = matches["sentences"][sentence_index][str(i)]["end"]
                            # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                            # NPs遵循贪婪匹配
                            flag = True
                            for vp_item in VPs:
                                # if VP contains NP, remove this NP
                                if begin >= vp_item[1] and end <= vp_item[2]:
                                    flag = False
                                    break

                            if flag == False:
                                continue    
                            for item in sorted(NPs):
                                if begin >= item[1] and end <= item[2]:
                                    flag = False
                                    break
                                if begin <= item[1] and end >= item[2]:
                                    NPs.remove(item)
                            # print(text, begin, end, flag)
                            if flag:
                                # print([text,begin,end])
                                # if text not in NP_set:
                                #     NP_set.add(text)
                                #     NPs.append([text,begin,end])
                                pattern_list.append(["NP", p_index, text])
                                NPs.append([text,begin,end])

                                
                # for item in pattern_list:
                #     print(item)
                # noun phrase extension
                # print("hehe")
                # NPs.extend(NP_extension_1(input_sentence, tokens, dependency_rel, NPs))
                # remove overlapped phrases in VPs
                for n_item in NPs:
                    n_begin = n_item[1]
                    n_end = n_item[2]
                    for v_item in VPs:
                        if (v_item[1] > n_begin and v_item[2] <= n_end) or (v_item[1] >= n_begin and v_item[2] < n_end):
                            VPs.remove(v_item)
                

                extended_NPs_1 = NP_extension_1(input_sentence, tokens, dependency_rel, NPs)
                NPs = remove_overlap(NPs, extended_NPs_1)

                extended_NPs_2 = NP_extension_2(input_sentence, tokens, dependency_rel, NPs)
                NPs = remove_overlap(NPs, extended_NPs_2)



                # print("NPs:", NPs)
                # print("VPs:", VPs)

                

                generated_triples = scenarios.Scenario(input_sentence, dependency_rel, VPs, NPs)

                for generated_triple in generated_triples:
                    # print(generated_triple)
                    triple = [sent_id, raw_sentence, generated_triple[1], generated_triple[0], generated_triple[2]]
                    sce_index = generated_triple[3]
                    sce_dist[sce_index] += 1

                    candidate_relation_triples.append(triple)
                # candidate_relation_triples.extend(scenarios.Scenario(dependency_rel, VPs, NPs))

    # for i in range(1, 10):
    #     print("sce_" + str(i) + " has: ", sce_dist[i])

    return candidate_relation_triples
    
        


if __name__ == "__main__":
    
    # input_contents = [
    #         1,
    #         "Bell , a telecommunication company , which is based in Los Angeles , makes and distributes electronic , computer and building products.",
    #     ]
    input_contents = [
            1,
            # "Bell , a telecommunication company , which is based in Los Angeles , makes and distributes electronic , computer and building products.",
            # "Rome, the capital of Italy, is known for the rich history",
            # "Shanghai is known for the modernization, which is in the east of China.",
            # "He has a bike.",
            # "Huawei, a leading global provider of informational and communicational technology and infrastructure, which is located in Shenzhen, is committed to building an intelligent and fully-connected world.",
            # "Yao Ming is a basketball player, who is born in Shanghai.",
            # "Bell, a telecommunication company, which is based in Los Angeles",
            # "Eclipse on your system can be used as a Java editor and a C++ editor",
            # "Rome is the capital of Italy and is known for rich history",
            # "Roger Federer is a tennis player, who was born in Basel, Switzerland",
            # "Roger Federer is a tennis player. He was born in Switzerland.",
            # "Sen. Mitchell is confident he has sufficient votes to block such a measure with procedural actions.",
            # "A large gravestone was erected in 1866 , over 100 years after his death.",
            # "Lugo and Lozano were released in 1993 and continue to reside in Venezuela.",
            # "23.8 % of all households were made up of individuals and 13.0 % had someone living alone who was 65 years of age or older",
            # "In 1879 , he was re-elected U.S. Senator and was tipped as a Presidential candidate , but died suddenly after giving a speech in Chicago .",
            # "He served as the first prime minister of Australia and became a founding justice of the High Court of Australia",
            # "`` I wo n't be throwing 90 mph , but I will throw 80 - plus , '' he says .",
            # "`` It is really bizarre , '' says Albert Lerman , creative director at the Wells Rich Greene ad agency .",
            "If he wins five key states, Republican candidate Mitt Romney will be elected President in 2008."
        ]    
    input_sentences = list()
    input_sentences.append(coref.pre_process_text(input_contents))
    # with open("../C2S_part/input.txt", "w", encoding="utf-8") as wf:
    #     for sentence in input_sentences:
    #         wf.write(sentence.strip()+"\n")
    #     wf.write("\n")

    
    candidate_relation_triples = chunk_candidate_relation_triples(input_sentences)
    print("input sentences:", input_sentences)
    for triple in candidate_relation_triples:
        # print(triple)
        print([triple[3], triple[2], triple[4]])