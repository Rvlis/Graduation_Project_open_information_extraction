"""
Implementation 6 scenarios, I noticed that some scen are similarly, such as 1 and 4, 2 and 3.
So there are less than 6 scenarios's detailed code. 
"""

def is_nsubjpass(source, target, vp, np):
    """
    :param source: int, dep_edge's source node
    :param target: int, dep_edge's target node
    :param vp: list[text, start, end], source maybe in text
    :param np: list[], target maybe in text

    :return true|false
    """
    # pass
    if source >= vp[1] and source < vp[2]:
        if target >= np[1] and target < np[2]:
            return True
    return False


def is_cop(source, target, np, vp):
    if source >= np[1] and source < np[2]:
        if target >= vp[1] and target < vp[2]:
            return True
    return False

def is_nsubj(source, target, np1, np2):
    if source >= np1[1] and source < np1[2]:
        if target >= np2[1] and target < np2[2]:
            return True
    return False

def is_dobj(source, target, vp, np):
    # pass
    if source >= vp[1] and source < vp[2]:
        if target >= np[1] and target < np[2]:
            return True
    return False


def is_nmod_or_obl(source, target, vp, np):
    # pass
    if source >= vp[1] and source < vp[2]:
        if target >= np[1] and target < np[2]:
            return True
    return False


def is_dep_or_xcomp(source, target, vp1, vp2):
    # pass
    if source >= vp1[1] and source < vp1[2]:
        if target >= vp2[1] and target < vp2[2]:
            return True
    return False

def is_appos(source, target, np1, np2):
    if source >= np1[1] and source < np1[2]:
        if target >= np2[1] and target < np2[2]:
            return True
    return False

# S.4 can also be implemented by this func.
def Scenario_1(input_sentence, dependency_rel, VPs, NPs):
    """
    :param dependency_rel: list[source_index, target_index, dependency]
    :param VPs: list[text, start, end], VP by rule-based chunking
    :param NPs: list[text, start, end], NP by rule-based chunking

    :return cadidate_relations_triples: list[VP, NP, VP]
    """

    candidate_relations_triples = list()
    
    # s.1 includes two dependencise: nsubj and dobj
    nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"] 
    dobj = [item for item in dependency_rel if item[2] == "dobj" or item[2] == "obj"]

    for n_item in nsubjpass:
        n_source = n_item[0]
        n_target = n_item[1]
        for vp in VPs:
                for np_1 in NPs:
                    if is_nsubjpass(n_source, n_target, vp, np_1):
                        for d_item in dobj:
                            d_source = d_item[0]
                            d_target = d_item[1]
                            for np_2 in NPs:
                                # excape overlap between np_1 and np_2
                                if np_2[0] == np_1[0]:
                                    continue
                                if d_source >= vp[1] and d_source <=vp[2] and is_dobj(d_source, d_target, vp, np_2):
                                    # candidate_relations_triples.append(["S1",np_1[0],vp[0],np_2[0]])
                                    if str(np_1[0]+" "+vp[0]+" "+np_2[0]) not in candidate_relation_triples_set:
                                        candidate_relations_triples.append([np_1[0],vp[0],np_2[0], 1])
                                        candidate_relation_triples_set.add(str(np_1[0]+" "+vp[0]+" "+np_2[0])) 
    # print("nsubjpass is ",nsubjpass)
    # for n_item in nsubjpass:
    #     n_source = n_item[0]
    #     n_target = n_item[1]
    #     for vp in VPs:
    #         if n_source >= vp[1] and n_source < vp[2]:
    #             for np_1 in NPs:
    #                 if n_target >= np_1[1] and n_target < np_1[2]:
    #                     for d_item in dobj:
    #                         d_source = d_item[0]
    #                         d_target = d_item[1]
    #                         if d_source >= vp[1] and d_source < vp[2]:
    #                             for np_2 in NPs:
    #                                 if d_target >= np_2[1] and d_target < np_2[2]:
    #                                     candidate_relations_triples.append([np_1[0],vp[0],np_2[0]])

    # print(candidate_relations_triples)
    return candidate_relations_triples


def Scenario_2(input_sentence, dependency_rel, VPs, NPs):
    """
    todo:
        Notice that with the preposition of dependency “nmod:at”, 
        the preposition of VP1 “is_developed_by” can be changed to “at” while chunking the second relation triples.
    """
    candidate_relations_triples = list()

    # two dependicies: nsubj and nmod or obl
    # nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"]
    nsubjpass = [item for item in dependency_rel if "nsubj" in item[2]] 
    # nmod_obl = [item for item in dependency_rel if item[2].find("nmod") != -1 or item[2].find("obl") != -1]
    nmod_obl = [item for item in dependency_rel if "nmod" in item[2] or "obl" in item[2]]


    for n_item in nsubjpass:
        n_source = n_item[0]
        n_target = n_item[1]
        for vp in VPs:
                for np_1 in NPs:
                    if is_nsubjpass(n_source, n_target, vp, np_1):
                        for d_item in nmod_obl:
                            d_source = d_item[0]
                            d_target = d_item[1]
                            for np_2 in NPs:
                                if np_2[0] == np_1[0]:
                                    continue
                                if d_source == n_source and is_dobj(d_source, d_target, vp, np_2):
                                    # candidate_relations_triples.append(["S2",np_1[0],vp[0],np_2[0]])
                                    if str(np_1[0]+" "+vp[0]+" "+np_2[0]) not in candidate_relation_triples_set:
                                        candidate_relations_triples.append([np_1[0],vp[0],np_2[0], 2])
                                        candidate_relation_triples_set.add(str(np_1[0]+" "+vp[0]+" "+np_2[0]))
    return candidate_relations_triples

def Scenario_3(input_sentence, dependency_rel, VPs, NPs):
    pass
    # can be implemented by S2

    # candidate_relations_triples = list()

    # nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"] 
    # nmod_obl = [item for item in dependency_rel if item[2].find("nmod") != -1 or item[2].find("obl") != -1]

    # for n_item in nsubjpass:
    #     n_source = n_item[0]
    #     n_target = n_item[1]
    #     for vp in VPs:
    #             for np_1 in NPs:
    #                 if is_nsubjpass(n_source, n_target, vp, np_1):
    #                     for d_item in nmod_obl:
    #                         d_source = d_item[0]
    #                         d_target = d_item[1]
    #                         for np_2 in NPs:
    #                             if is_dobj(d_source, d_target, vp, np_2):
    #                                 candidate_relations_triples.append([np_1[0],vp[0],np_2[0]]) 

    # # print(candidate_relations_triples)
    # return candidate_relations_triples

def Scenario_4(input_sentence, dependency_rel, VPs, NPs):
    # can be implemented by S.1
    pass

def Scenario_5(input_sentence, dependency_rel, VPs, NPs):

    candidate_relations_triples = list()
    candidate_relations_triples.extend(Scenario_2(input_sentence, dependency_rel, VPs, NPs))

    nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"] 
    dep_xcomp = [item for item in dependency_rel if item[2] == "dep" or item[2] == "xcomp"]
    dobj = [item for item in dependency_rel if item[2] == "dobj" or item[2] == "obj"]

    for n_item in nsubjpass:
        n_source = n_item[0]
        n_target = n_item[1]
        for vp_1 in VPs:
                for np_1 in NPs:
                    if is_nsubjpass(n_source, n_target, vp_1, np_1):
                        for d_item in dep_xcomp:
                            d_source = d_item[0]
                            d_target = d_item[1]
                            for vp_2 in VPs:
                                if is_dep_or_xcomp(d_source, d_target, vp_1, vp_2):
                                    # candidate_relations_triples.append([np_1[0],vp[0],np_2[0]]) 
                                    for dobj_item in dobj:
                                        dobj_source = dobj_item[0]
                                        dobj_target = dobj_item[1]
                                        for np_2 in NPs:
                                            if np_2[0] == np_1[0]:
                                                continue
                                            if d_target == dobj_source and is_dobj(dobj_source, dobj_target, vp_2, np_2):
                                                # candidate_relations_triples.append(["S5",np_1[0],vp_2[0],np_2[0]])
                                                if str(np_1[0]+" "+vp_2[0]+" "+np_2[0]) not in candidate_relation_triples_set:
                                                    candidate_relation_triples_set.add(str(np_1[0]+" "+vp_2[0]+" "+np_2[0]))
                                                    candidate_relations_triples.append([np_1[0],vp_2[0],np_2[0], 5])

    # print(candidate_relations_triples)
    return candidate_relations_triples


# additional scenario: appositions
def Scenario_6(input_sentence, dependency_rel, VPs, NPs):
    """
    Scenario_6 is used to handle appositions relation

    :param dependency_rel: list[source_index, target_index, dependency]
    :param VPs: list[text, start, end], VP by rule-based chunking
    
    :return cadidate_relations_triples: list[NP, "is", NP]
    """
    candidate_relation_triples = list()
    appos = [item for item in dependency_rel if item[2] == "appos"]

    #1 "Bell , a telecommunication company"
    # SVO, here V is 'is'
    for item in appos:
        n_source = item[0]
        n_target = item[1]
        for np_1 in NPs:
            for np_2 in NPs:
                if np_1[0] == np_2[0]:
                    continue
                if is_appos(n_source, n_target, np_1, np_2):
                    if str(np_1[0]+" "+ "is" +" "+np_2[0]) not in candidate_relation_triples_set:
                        candidate_relation_triples_set.add(str(np_1[0]+" "+ "is" +" "+np_2[0]))
                        candidate_relation_triples.append([np_1[0], '"is" ', np_2[0], 6])

    #2 "Rome, the capital of Italy"
    # SVOO, here O1 is 'capital', O2 is 'Italy'
    nmod = [item for item in dependency_rel if "nmod" in item[2]]
    for a_item in appos:
        a_source = a_item[0]
        a_target = a_item[1]
        for np_1 in NPs:
            for vp in VPs:
                if is_appos(a_source, a_target, np_1, vp):
                    for n_item in nmod:
                        n_source = n_item[0]
                        n_target = n_item[1]
                        for np_2 in NPs:
                            if np_2[0] == np_1[0]:
                                continue
                            if is_nmod_or_obl(n_source, n_target, vp, np_2):
                                if str(np_1[0]+" "+ "is "+vp[0]+" "+np_2[0]) not in candidate_relation_triples_set:
                                    candidate_relation_triples_set.add(str(np_1[0]+" "+ "is"+" "+vp[0]+" "+np_2[0]))
                                    candidate_relation_triples.append([np_1[0], '"is"'+" "+vp[0], np_2[0], 6])
                

    return candidate_relation_triples

# additional scenario: possessives
# def Scenario_7(input_sentence, dependency_rel, NPs):
#     """
#     Scenario_7 is used to handle complicated possessives relation

#     :param dependency_rel: list[source_index, target_index, dependency]
#     :param VPs: list[text, start, end], VP by rule-based chunking
#     :param NPs: list[text, start, end], NP by rule-based chunking

#     :return cadidate_relations_triples: list[NP, "has", VP]
#     """
#     candidate_relation_triples = list()
#     # 
#     poss = [item for item in dependency_rel if item[2] == "nmod:poss"]

#     poss_dict = {
#         "my": "I",
#         "your": "you",
#         "his": "he",
#         "her": "she",
#         "its": "it",
#         "our": "we",
#         "their": "they",

#         "mine": "I",
#         "yours": "you",
#         "hers": "she",
#         "ours": "we",
#         "theirs": "they"
#     }

#     for item in poss:
#         n_source = item[0]
#         n_target = item[1]
#         for np_1 in NPs:
#             pass           


# additional scenario: conj between two defferent vp
def Scenario_7(input_sentence, dependency_rel, VPs, raw_candidate_relations_triples):
    """
    Scenario_7 is used to handle conj relation between two different vp

    :param dependency_rel: list[source_index, target_index, dependency]
    :param VPs: list[text, start, end], VP by rule-based chunking
    :param NPs: list[text, start, end], NP by rule-based chunking

    :return cadidate_relations_triples: list[NP, "has", VP]
    """
    candidate_relation_triples = list()
    # conj:and only
    conj = [item for item in dependency_rel if item[2] == "conj:and"]
    for item in conj:
        n_source = item[0]
        n_target = item[1]
        for vp_1 in VPs:
            if n_source >= vp_1[1] and n_source < vp_1[2]:
                source_vp = vp_1[0]
                for vp_2 in VPs:
                    if n_target >= vp_2[1] and n_target < vp_2[2]:
                        target_vp = vp_2[0]
                        # escape overlap
                        if target_vp == source_vp:
                            continue
                        for item in raw_candidate_relations_triples:
                            if item[1] == source_vp:
                                candidate_relation_triples_set.add(str(item[0] + " " + target_vp + " " + item[2]))
                                candidate_relation_triples.append([item[0], target_vp, item[2], 7])
    return candidate_relation_triples

def Scenario_8(input_sentence, dependency_rel, VPs, NPs, raw_candidate_relations_triples):
    # cop
    candidate_relation_triples = list()
    cop = [item for item in dependency_rel if item[2] == "cop"]
    nsubj = [item for item in dependency_rel if item[2] == "nsubj"]
    for c_item in cop:
        c_source = c_item[0]
        c_target = c_item[1]
        for vp in VPs:
                for np_1 in NPs:
                    if is_cop(c_source, c_target, np_1, vp):
                        for n_item in nsubj:
                            n_source = n_item[0]
                            n_target = n_item[1]
                            for np_2 in NPs:
                                # excape overlap between np_1 and np_2
                                if np_2[0] == np_1[0]:
                                    continue
                                if is_nsubj(n_source, n_target, np_1, np_2):
                                    # candidate_relations_triples.append(["S1",np_1[0],vp[0],np_2[0]])
                                    if str(np_2[0]+" "+vp[0]+" "+np_1[0]) not in candidate_relation_triples_set:
                                        candidate_relation_triples.append([np_2[0],vp[0],np_1[0], 8])
                                        candidate_relation_triples_set.add(str(np_2[0]+" "+vp[0]+" "+np_1[0])) 
    return candidate_relation_triples

def Scenario_9(input_sentence, dependency_rel, VPs, NPs, raw_candidate_relations_triples):
    # cop
    candidate_relation_triples = list()
    cop = [item for item in dependency_rel if item[2] == "cop"]
    nsubj = [item for item in dependency_rel if item[2] == "nsubj"]
    for c_item in cop:
        c_source = c_item[0]
        c_target = c_item[1]
        for vp in VPs:
                for np_1 in NPs:
                    if is_cop(c_source, c_target, np_1, vp):
                        for n_item in nsubj:
                            n_source = n_item[0]
                            n_target = n_item[1]
                            for np_2 in NPs:
                                # excape overlap between np_1 and np_2
                                if np_2[0] == np_1[0]:
                                    continue
                                if is_nsubj(n_source, n_target, np_1, np_2):
                                    # candidate_relations_triples.append(["S1",np_1[0],vp[0],np_2[0]])
                                    if str(np_2[0]+" "+vp[0]+" "+np_1[0]) not in candidate_relation_triples_set:
                                        candidate_relation_triples.append([np_2[0],vp[0],np_1[0], 9])
                                        candidate_relation_triples_set.add(str(np_2[0]+" "+vp[0]+" "+np_1[0])) 
    return candidate_relation_triples 

candidate_relation_triples_set = set()
def Scenario(input_sentence, dependency_rel, VPs, NPs):
    # all scenarios
    candidate_relations_triples = list()
    candidate_relations_triples.extend(Scenario_1(input_sentence, dependency_rel, VPs, NPs))
    # candidate_relations_triples.extend(Scenario_3(dependency_rel, VPs, NPs))
    candidate_relations_triples.extend(Scenario_5(input_sentence, dependency_rel, VPs, NPs))
    candidate_relations_triples.extend(Scenario_6(input_sentence, dependency_rel, VPs, NPs))
    # candidate_relations_triples.extend(Scenario_7(dependency_rel, NPs))
    candidate_relations_triples.extend(Scenario_7(input_sentence, dependency_rel, VPs, candidate_relations_triples))
    candidate_relations_triples.extend(Scenario_8(input_sentence, dependency_rel, VPs, NPs, candidate_relations_triples))
    candidate_relations_triples.extend(Scenario_9(input_sentence, dependency_rel, VPs, NPs, candidate_relations_triples))

    return candidate_relations_triples