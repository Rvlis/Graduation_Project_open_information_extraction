import os
import sys

sys.path.append(".")
sys.path.append("./C2S_part/")  #文本简化
sys.path.append("./NER_part/")  #实体识别

from tqdm import tqdm
import argparse
from NER_part import corenlp_chunk_candidate_relations_triples, coref



def coref_resolve(is_coref, contents):
    """
    resolving coreference
    :param is_coref: args.coref, Judge resolving coreference, [0, 1]
    :param contents: list, raw sentences
    :return input_sentences: list, [sent_id, content, resolving_content] or [sent_id, content, content]
    """
    input_sentences = list()
    contents = list(enumerate(list(contents), start=1))
    for content in tqdm(contents):
        # print("content:", content)
        if is_coref == 1:
            input_sentences.append(coref.pre_process_text(list(content)))
        else:
            content = list(content)
            content.insert(2, content[1])
            input_sentences.append(content)
    return input_sentences

def text_simplify(is_simp, input_sentences):
    """
    reso
    :param is_simp: args.simp, Judge simplifying text
    :param input_sentences: list, [sent_id, content, resolving content] or [sent_id, content, content]
    :return simplified_sentences: list, [sent_id, content_0, simplified_sentence_01], [sent_id, content_0, simplified_sentence_02], ..., [sent_id, content_n, simplified_sentence_ni]  
    """
    simplified_sentences = list()
    if is_simp == 1:
        with open("../data/C2S_input.txt", "w", encoding="utf-8") as wf:
            for item in input_sentences:
                sent_id = item[0]
                raw_sentence = item[1]
                coref_resolved_sentence = item[2].strip().replace("\n", " ").replace("\t", " ")
                wf.write(raw_sentence)


        os.system("mvn -q -f ./C2S_part/pom.xml clean compile exec:java")
        
        with open("../data/C2S_output.txt", encoding="unicode_escape") as rf:
            sent_id = 0
            last_sentence = ""
            for line in rf:
                # simplified_sentences: list, [[sent_id, raw_sentence, simplified_clause_sentence], ...]
                raw_sentence = line.split("\t")[0]
                if raw_sentence != last_sentence:
                    sent_id += 1
                    last_sentence = raw_sentence
                simplified_sentence = [sent_id, line.split("\t")[0], line.split("\t")[3]]
                # print(simplified_sentence)
                simplified_sentences.append(simplified_sentence)
    else:
        simplified_sentences = input_sentences
    return simplified_sentences

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--coref", type=int, default=1, choices=[0,1], help="Whether turn on coreference resolution or not")
    parser.add_argument("-s", "--simp", type=int, default=1, choices=[0,1], help="Whether turn on c2s or not")
    args = parser.parse_args()
    # contents = """The 2006 Pangandaran earthquake and tsunami occurred on July 17 at along a subduction zone off the coast of Java, a large and densely populated island in the Indonesian archipelago. The shock had a moment magnitude of 7.7 in Jakarta, which is the capital of Indonesia. There were no direct effects of the earthquake's shaking due to its low intensity, and the large loss of life from the event was due to the resulting tsunami, which inundated a portion of the Java coast that had been unaffected by the earlier 2004 Indian Ocean earthquake and tsunami that was off the coast of Sumatra. The July 2006 earthquake was also centered in the Indian Ocean, from the coast of Java, and had a duration of more than three minutes. An abnormally slow rupture at the Sunda Trench and a tsunami that was unusually strong relative to the size of the earthquake were both factors that led to it being categorized as a tsunami earthquake. Several thousand kilometers to the southeast, surges of several meters were observed in northwestern Australia, but in Java the tsunami heights above normal sea level were typically and resulted in the deaths of more than 600 people. Other factors may have contributed to exceptionally high peak runups of on the small and mostly uninhabited island of Nusa Kambangan, just to the east of the resort town of Pangandaran, where damage was heavy and a large loss of life occurred. Since the shock was felt with only moderate intensity well inland, and even less so at the shore, the surge arrived with little or no warning. Other factors contributed to the tsunami being largely undetected until it was too late and, although a tsunami watch was posted by an American tsunami warning center and a Japanese meteorological center, no information was delivered to people at the coast."""
    
    # print("hello")
    # all
    # with open("./Preprocess_part/data/OpenIE_test.txt", encoding="utf-8") as contents: 
    # benchie-30
    with open("./Preprocess_part/data/benchie-30.txt", encoding="utf-8") as contents:
        # input_sentences, list, [[content, sent1, sent2, ....], [content, sent1, sent2, ....]]
        input_sentences = list()
        
        # step 1): resolving coreference
        input_sentences = coref_resolve(args.coref, contents)
    
        # if args.coref == 1:    
        #     print("-------------------- Resolving Coreference --------------------")
        #     contents = list(enumerate(list(contents), start=1))
        #     # print("contents:", contents)
            
        #     for content in tqdm(contents):
        #         input_sentences.append(coref.pre_process_text(list(content)))
        # else:
        #     contents = list(enumerate(list(contents), start=1))
        #     for content in tqdm(contents):
        #         content = list(content)
        #         content.insert(2, content[1])
        #         print("content:", content)
        #         input_sentences.append(content)


        # step 2): Simplifying text

        simplified_sentences = text_simplify(args.simp, input_sentences)
        # print("simplified_sentences:", simplified_sentences)
        # if args.simp == 1:
        #     with open("../data/C2S_input.txt", "w", encoding="utf-8") as wf:
        #         for item in input_sentences:
        #             sent_id = item[0]
        #             raw_sentence = item[1]
        #             coref_resolved_sentence = item[2].strip().replace("\n", " ").replace("\t", " ")
        #             wf.write(raw_sentence)

        #     os.system("mvn -q -f ./C2S_part/pom.xml clean compile exec:java")
        #     simplified_sentences = list()
        #     with open("../data/C2S_output.txt", encoding="unicode_escape") as rf:
        #         sent_id = 0
        #         last_sentence = ""
        #         for line in rf:
        #             # simplified_sentences: list, [[sent_id, raw_sentence, simplified_clause_sentence], ...]
        #             raw_sentence = line.split("\t")[0]
        #             if raw_sentence != last_sentence:
        #                 sent_id += 1
        #                 last_sentence = raw_sentence
        #             simplified_sentence = [sent_id, line.split("\t")[0], line.split("\t")[3]]
        #             # print(simplified_sentence)
        #             simplified_sentences.append(simplified_sentence)
        # else:
        #     simplified_sentences = input_sentences


        # print("sent_id: ", sent_id)
        # print(simplified_sentences)

        # step 3): extracting relation triples
        candidate_relation_triples = corenlp_chunk_candidate_relations_triples.chunk_candidate_relation_triples(simplified_sentences)
        # for triple in candidate_relation_triples:
        #     print(triple)


        # CaRB benchmark
        # with open("../data/CaRB_output.txt", "w", encoding="utf-8") as wf:
        #     for triple in candidate_relation_triples:
        #         tmp_triple = list()
        #         # note: CaRB Tab Seperated: sent, prob, pred, arg1, arg2, add prob to triples
        #         tmp_triple.insert(0, triple[1].strip())
        #         tmp_triple.insert(1, "1.0")
        #         tmp_triple.insert(2, triple[2].strip())
        #         tmp_triple.insert(3, triple[3].strip())
        #         tmp_triple.insert(4, triple[4].strip())

        #         # print(tmp_triple)

        #         wf.write("\t".join(tmp_triple)+"\n")


        # Benchie benchmark
        with open("../data/benchie_30_output.txt", "w", encoding="utf-8") as wf:
            for triple in candidate_relation_triples:
                # triple: list, [sent_id, raw_sentence, VP, NP1, NP2]
                triple[0], triple[1] = triple[1], triple[0]
                triple[2], triple[3] = triple[3], triple[2]
                triple[1] = str(triple[1])
                # print(triple, triple[1:])


                wf.write("\t".join(triple[1:])+"\n")
        
        # os.system("pause")
        # atomic proposition with the position of head and tail: [sentence, [start, end], [start, end]]
        # atomic_propositions = list()
        # with open("../data/atomic_propositions.txt", "w", encoding="utf-8") as wf:    
        #     for relation_triple in candidate_relation_triples:
        #         h_start = 0
        #         h_end = len(relation_triple[0])
        #         t_start = len(relation_triple[0])+1 + len(relation_triple[1])+1
        #         t_end = len(relation_triple[0])+1 + len(relation_triple[1])+1 + len(relation_triple[2])
        #         atomic_proposition = [str(relation_triple[0] + " " + relation_triple[1] + " " + relation_triple[2]), [h_start, h_end], [t_start, t_end]]
        #         # print(atomic_proposition) 
        #         wf.write(str(relation_triple[0] + " " + relation_triple[1] + " " + relation_triple[2]) + "\t" + str(h_start) + "\t" + str(h_end) + "\t" + str(t_start) + "\t" + str(t_end) + "\n")
