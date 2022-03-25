import os
import sys


def text_simplify(is_simp, input_sentences, DIR_PATH):
    """
    reso
    :param is_simp: args.simp, Judge simplifying text
    :param input_sentences: list, [sent_id, content, resolving content] or [sent_id, content, content]
    :return simplified_sentences: list, [sent_id, content_0, simplified_sentence_01], [sent_id, content_0, simplified_sentence_02], ..., [sent_id, content_n, simplified_sentence_ni]  
    """
    simplified_sentences = list()
    if is_simp == 1:
        with open(os.path.join(DIR_PATH, "data/C2S_input.txt"), "w", encoding="utf-8") as wf:
            for item in input_sentences:
                sent_id = item[0]
                raw_sentence = item[1]
                coref_resolved_sentence = item[2].strip().replace("\n", " ").replace("\t", " ")
                wf.write(raw_sentence)

        # print("mvn -q -f {} clean compile exec:java".format(os.path.join(DIR_PATH, "src/C2S_part/pom.xml")))
        os.system("mvn -q -f {} clean compile exec:java".format(os.path.join(DIR_PATH, "src/C2S_part/pom.xml")))
        
        with open(os.path.join(DIR_PATH, "data/C2S_output.txt"), encoding="unicode_escape") as rf:
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
