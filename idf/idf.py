import os
import operator
from math import log
from collections import Counter
from pprint import pprint
import pickle
import sys
import json

cur_dir = os.path.dirname(os.path.realpath(__file__))
chr_map = {"chr1": 0,
           "chr2": 249250621,
           "chr3": 492449994,
           "chr4": 690472424,
           "chr5": 881626700,
           "chr6": 1062541960,
           "chr7": 1233657027,
           "chrX": 1392795690,
           "chr8": 1548066250,
           "chr9": 1694430272,
           "chr10": 1835643703,
           "chr11": 1971178450,
           "chr12": 2106184966,
           "chr13": 2240036861,
           "chr14": 2355206739,
           "chr15": 2462556279,
           "chr16": 2565087671,
           "chr17": 2655442424,
           "chr18": 2736637634,
           "chr20": 2814714882,
           "chrY": 2877740402,
           "chr19": 2937113968,
           "chr22": 2996242951,
           "chr21": 3047547517,
           "chrM": 3095677412}

def bed_generate(bedfile, need_score=False):
    with open(bedfile) as bf:
        for i in bf:
            isp = i.strip().split()
            try:
                term = (int(isp[1]) + chr_map[isp[0]]) // 10000
            except KeyError as k:
                print(k)
                continue

            if need_score:
                yield term, float(isp[4])
            else:
                yield term


class TfIdf:
    def __init__(self, tab):
        self.bedfiles = []
        with open(tab) as tab_f:
            for i in tab_f:
                path = i.strip().split()[2]
                if os.path.exists(path):
                    self.bedfiles.append(path)
        self.idf_for_term = dict()
        self.tf_score_in_doc = dict()
        self.tf_idf_in_doc = dict()

    def cal_idf(self):
        contain_term_cnt = dict()
        total_cnt = len(self.bedfiles)

        # count number of documents containing a term
        for bed in self.bedfiles:
            counted = set()
            for term in bed_generate(bed):
                if term not in counted:
                    contain_term_cnt[term] = contain_term_cnt.get(term, 0) + 1
                    counted.add(term)

        for term in contain_term_cnt:
            self.idf_for_term[term] = log(total_cnt / (contain_term_cnt[term]))

    def cal_tf(self):
        for bed in self.bedfiles:
            self.tf_score_in_doc[bed] = {}
            max_score = 0
            for term, score in bed_generate(bed, need_score=True):
                self.tf_score_in_doc[bed][term] = score
                max_score = max(score, max_score)

            for term in self.tf_score_in_doc[bed]:
                self.tf_score_in_doc[bed][term] /= max_score

    def cal_tf_idf(self):
        for bed in self.bedfiles:
            self.tf_idf_in_doc[bed] = dict()
            for term in self.tf_score_in_doc[bed]:
                self.tf_idf_in_doc[bed][term] = self.tf_score_in_doc[bed][term] * self.idf_for_term[term]

    def get_most_important(self, n):
        ret = dict()
        for bed in self.bedfiles:
            ret[bed] = {i[0] for i in sorted(self.tf_idf_in_doc[bed].items(), key=lambda x: x[1])[-n:]}
        return ret


def get_overlap(bedfile, most_important):
    cur_set = set()
    for term in bed_generate(bedfile):
        cur_set.add(term)

    ret = []
    for bed in most_important:
        bed_id = bed[bed.rfind("/")+1:]
        bed_id = bed_id[:bed_id.find("_")]
        ret.append([bed_id, len(most_important[bed].intersection(cur_set))])
    return ret

import time


try:
    most_imp = pickle.load(open(os.path.join(cur_dir,"most_imp"), "rb"))
    print("read from file", file=sys.stderr)
except:
    my_tfidf = TfIdf("/Users/ad9075/Downloads/Sandbox/idf/Data/Juan_H3K27me3.tab")
    my_tfidf.cal_tf()
    my_tfidf.cal_idf()
    my_tfidf.cal_tf_idf()
    most_imp = my_tfidf.get_most_important(1000)
    pickle.dump(most_imp, open("/Users/ad9075/Downloads/Sandbox/tfidf/idf/most_imp", "wb"))
    print("write into file", file=sys.stderr)

print(json.dumps(
    sorted(get_overlap(sys.argv[1], most_imp),key=lambda x: x[1], reverse=True)[:10]))
