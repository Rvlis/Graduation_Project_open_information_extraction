import os
import sys

sys.path.append("./")
sys.path.append("./Preprocess_part/")   #预处理-共指消解
sys.path.append("./C2S_part/")          #复合句简化
sys.path.append("./NER_part/")          #实体识别 + 关系抽取

DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("OIE文件夹路径：", DIR_PATH)

from tqdm import tqdm
import argparse
from Preprocess_part import coref
from C2S_part import text_simplify
from NER_part import corenlp_chunk_candidate_relations_triples


def single_extraction(args, content):
    """
    单句抽取
    """
    input_sentences = list()
        
    # step 1): 共指消解
    input_sentences = coref.coref_resolve(args.coref, content)

    # step 2): 文本简化
    simplified_sentences = text_simplify.text_simplify(args.simp, input_sentences, DIR_PATH)

    # step 3): 实体识别 + 关系抽取
    candidate_relation_triples = corenlp_chunk_candidate_relations_triples.chunk_candidate_relation_triples(simplified_sentences)
    for triple in candidate_relation_triples:
        print("{} --> ({}; {}; {})".format(triple[1], triple[3], triple[2], triple[4]))

def batch_extraction(args, input_path):
    """
    批量抽取
    input_path: 指定输入文件路径
    """
    with open(input_path, encoding="utf-8") as contents:
        # input_sentences, list, [[content, sent1, sent2, ....], [content, sent1, sent2, ....]]

        input_sentences = list()
        
        # step 1): 共指消解
        input_sentences = coref.coref_resolve(args.coref, contents)

        # step 2): 文本简化
        simplified_sentences = text_simplify.text_simplify(args.simp, input_sentences, DIR_PATH)

        # step 3): 实体识别 + 关系抽取
        candidate_relation_triples = corenlp_chunk_candidate_relations_triples.chunk_candidate_relation_triples(simplified_sentences)
        # for triple in candidate_relation_triples:
        #     print(triple)
    
    return candidate_relation_triples

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--coref", type=int, default=1, choices=[0,1], help="Whether turn on coreference resolution or not")
    parser.add_argument("-s", "--simp", type=int, default=1, choices=[0,1], help="Whether turn on c2s or not")
    parser.add_argument("-t", "--type", type=int, default=0, choices=[0,1], help="选择抽取类型：单句抽取（0），批量抽取（1）；默认单句抽取")
    args = parser.parse_args()

    # 单句抽取
    if args.type == 0:
        content = "Bell, a telecommunication company, which is based in Los Angeles"
        single_extraction(args, content)
    # 批量抽取
    else:
        candidate_relation_triples = batch_extraction(args, "../../CaRB/data/dev.txt")
        # candidate_relation_triples = batch_extraction("../../CaRB/data/test.txt")

    # step 4): 性能评估
    # CaRB benchmark
    with open("../data/CaRB_output_dev.txt", "w", encoding="utf-8") as wf:
    # with open("../data/CaRB_output_test.txt", "w", encoding="utf-8") as wf:
        for triple in candidate_relation_triples:
            tmp_triple = list()
            # note: CaRB Tab Seperated: sent, prob, pred, arg1, arg2, add prob to triples
            tmp_triple.insert(0, triple[1].strip())

            # 因为本方法没有设置置信度，此处设置为定值1.0即可，不影响评估效果
            # 带来的影响是：无法绘制不同置信度条件下的AUC曲线
            tmp_triple.insert(1, "1.0")
            tmp_triple.insert(2, triple[2].strip())
            tmp_triple.insert(3, triple[3].strip())
            tmp_triple.insert(4, triple[4].strip())
            wf.write("\t".join(tmp_triple)+"\n")
