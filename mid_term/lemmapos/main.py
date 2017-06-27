#! /usr/bin/python3

"""
@:param: NLSPARQL.train.feats.txt
@:param: NLSPARQL.train.data
@:param: NLSPARQL.test.feats.txt
@:param: NLSPARQL.test.data

OUTPUT

IOB_sentence.txt:       train sentences in IOB tags format
sentence.txt:           test sentences in lemma_pos format
lexicon.txt:            lexicon file
automa.txt:             automa transitions lemmapos - IOB tag

"""

import sys
import math
from collections import Counter

#read the train.feats
lemma_file = sys.argv[1]
#read the train file
train = sys.argv[2]

#read the test.feats file
test_feats = sys.argv[3]

#read the test file
test = sys.argv[4]

#file in which sentence-of-tag are saved
IOB_sentence = open("IOB_sentence.txt","w")

#file that contains all the sentencenses without the tag
sentences=open("sentences.txt","w")

iob_tags = []
merged_data = []
lemma_pos = []

with open(train, "r") as t:
    tmp = t.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            IOB_sentence.write(y + " ")
            iob_tags.append(y)
        else:
            IOB_sentence.write("\n")

with open(lemma_file, "r") as t:
    tmp = t.read().split('\n')
    for line in tmp:
        if line != '':
            x, y, z = line.split('\t')
            lemma_pos.append((z, y))


with open(test_feats, "r") as s:
    tmp=s.read().split('\n')
    for line in tmp:
        if line != '':
            x, y, z = line.split('\t')
            sentences.write(z+y +" ")
        else:
            sentences.write("\n")

with open(lemma_file, "r") as l, open(train, "r") as t:
    tmp_l = l.read().split('\n')
    tmp_t = t.read().split('\n')
    for line_lemma, line_train in zip(tmp_l,tmp_t):
        if line_lemma !='' and line_train!='':
            a,b = line_train.split('\t')
            x, y, z = line_lemma.split('\t')
            merged_data.append((z, y, b))


iob_tags_uniq = Counter(iob_tags)
merged_data_uniq = Counter(merged_data)
lemma_pos_uniq=Counter(lemma_pos)



#############################          CREATE THE LEXICON          ###############################

lexicon = open("lexicon.txt", "w")
counter_lexicon = 0
lexicon.write("<eps>"+"\t"+str(counter_lexicon)+"\n")


for i in lemma_pos_uniq:
    counter_lexicon +=1
    lexicon.write(i[0]+i[1]+"\t"+str(counter_lexicon)+"\n")
for i in iob_tags_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
counter_lexicon += 1
lexicon.write("<unk>"+"\t"+str(counter_lexicon))
lexicon.close()

#############################        AUTOMA     #################################################

#compute probilities/costs for the automata
probs_lemmapos_iob = []
for i in iob_tags_uniq:
    for y in lemma_pos_uniq:
        index = (y[0], y[1], i)
        if merged_data_uniq[index] != 0:
            prob = (merged_data_uniq[index]/iob_tags_uniq[i])
            if prob !=1 :
                probs_lemmapos_iob.append((y[0]+y[1], i, -(math.log(prob))))
            else:
                probs_lemmapos_iob.append((y[0]+y[1], i, 0.0))


#automa
automata1 = open("automa.txt", "w")
for i in probs_lemmapos_iob:
    automata1.write("0" + "\t" + "0" + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
    automata1.write("\n")
for i in iob_tags_uniq:
    automata1.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + i + "\t" + str(-math.log(1/iob_tags_uniq.__len__())))
    automata1.write("\n")

automata1.write("0")



