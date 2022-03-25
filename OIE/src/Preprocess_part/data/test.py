import jsonlines
import os

# s_cnt = 0
# with open("./train.jsonl", encoding="utf-8") as rf:
#     with open("./raw_text.txt", "w", encoding="utf-8") as wf:
#         for item in jsonlines.Reader(rf):
#             content = item["content"]
#             for sentence in content:
#                 # print(sentence["sentence"])
#                 wf.write(sentence["sentence"]+" ")
#                 s_cnt += 1
#             wf.write("\n")

# print(s_cnt)

s_cnt = 0
cnt = 1
with open("./test.jsonl", encoding="utf-8") as rf:
    with open("./KG_test.txt", "w", encoding="utf-8") as wf:
        for item in jsonlines.Reader(rf):
            content = item["content"]
            for sentence in content:
                # print(sentence["sentence"])
                wf.write(sentence["sentence"].replace("\t", " ")+" ")
                s_cnt += 1
            wf.write("\t")
            candidates = item["candidates"]
            for trigger_word in candidates:
                if cnt%3 == 0 or cnt%2 == 0:
                    # print("hehe")
                    wf.write(trigger_word["trigger_word"] + "\t")
                cnt += 1
            wf.write("\n")


print(s_cnt)