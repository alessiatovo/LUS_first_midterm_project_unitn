#! /usr/bin/python3

import sys
from collections import Counter

merged_train = open("data/merged_train.txt","w")

num = sys.argv[1]
length_suffix_prefix = int(3)

with open("data/NLSPARQL.train.data", "r") as d, open("data/NLSPARQL.train.feats.txt", "r") as f:
    tmp_d = d.read().split('\n')
    tmp_f = f.read().split('\n')
    for line_data, line_feats in zip(tmp_d,tmp_f):
        if line_data !='' and line_feats!='':
            word,iob = line_data.split('\t')
            c, pos, lemma = line_feats.split('\t')
            if len(word) >= length_suffix_prefix:
                prefix = word[0:length_suffix_prefix]
                suffix = word[-length_suffix_prefix:]
            else:
                prefix = str(None)
                suffix = str(None)
            merged_train.write(word + "\t" + lemma + "\t" + pos + "\t" + prefix + "\t" + suffix + "\t" + iob + "\n")
        else:
            merged_train.write("\n")



merged_test = open("data/merged_test.txt", "w")

with open("data/NLSPARQL.test.data", "r") as d, open("data/NLSPARQL.test.feats.txt", "r") as f:
    tmp_d = d.read().split('\n')
    tmp_f = f.read().split('\n')
    for line_data, line_feats in zip(tmp_d,tmp_f):
        if line_data !='' and line_feats!='':
            word,iob = line_data.split('\t')
            c, pos, lemma = line_feats.split('\t')
            if len(word) >= length_suffix_prefix:
                prefix = word[0:length_suffix_prefix]
                suffix = word[-length_suffix_prefix:]
            else:
                prefix = str(None)
                suffix = str(None)

            merged_test.write(word +"\t" +lemma+"\t"+ pos+ "\t"+prefix+"\t"+suffix+"\t"+ iob+ "\n")
        else:
            merged_test.write("\n")



