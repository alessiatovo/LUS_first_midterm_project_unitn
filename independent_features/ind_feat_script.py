#! /usr/bin/python3
"""
INSTRUCTIONS

three automata are been generated:
   first automa:     transition word-lemma
   second automa:    transition lemma-pos_tag
   third automa:     transition pos_tag-iob_tag

independent features assumptions are made in this train

parameters taken from input line

@param1: NLSPARQL.train.feats.txt
@param2: NLSPARQL.train.data.txt
@param3: NLSPARQL.test.data.txt

OUTPUT generated:
    IOB_sentence.txt:           contains train sentences written in IOB tag format
    sentences.txt:              contains test sentences, one sentences per line
    lexicon_lemmatization.txt:  lexicon file
    automata_1.txt:             first automa for transition word - lemmma
    automata_2.txt:             second automa for transition lemma - pos-tag
    automata_3.txt:             third automa for transition pos-tag - iob-tag

"""
import sys
import math
from collections import Counter

#read the train lemma
lemma_file = sys.argv[1]
#read the train file
train = sys.argv[2]
#read the test file
test = sys.argv[3]

file_data_lemma = []
file_data_train = []
#file in which sentence-of-tag are saved
IOB_sentence = open("IOB_sentence.txt","w")
#file that contains all the sentencenses without the tag
sentences=open("sentences.txt","w")
#POS tag and IOB tags couple coming from train.feats.data
#POS_IOB_tags = {}
iob_tags = []
pos_tag = []
lemmas= []
word_lemma = []
words = []
merged_data = []
tmp_map = {}
lemma_pos = []

with open(lemma_file, "r") as f:
    tmp = f.read().split('\n')
    for line in tmp:
        if line != '':
            x, y, z = line.split('\t')
            file_data_lemma.append((x,y,z))
            pos_tag.append(y)
            lemmas.append(z)
            word_lemma.append((x, z))
            words.append(x)
            lemma_pos.append((z, y))

with open(train, "r") as t:
    tmp = t.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            IOB_sentence.write(y + " ")
            file_data_train.append((x, y))
            iob_tags.append(y)
        else:
            IOB_sentence.write("\n")

with open(test, "r") as s:
    tmp=s.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            sentences.write(x +" ")
        else:
            sentences.write("\n")

with open(lemma_file, "r") as l, open(train, "r") as t:
    tmp_l = l.read().split('\n')
    tmp_t = t.read().split('\n')
    for line_lemma, line_train in zip(tmp_l,tmp_t):
        if line_lemma !='' and line_train!='':
            a,b = line_train.split('\t')
            x, y, z = line_lemma.split('\t')
            merged_data.append((a, z, y, b))



iob_tags_uniq = Counter(iob_tags)
pos_tags_uniq = Counter(pos_tag)
lemmas_uniq = Counter(lemmas)
word_lemma_uniq = Counter(word_lemma)
words_uniq = Counter(words)
merged_data_uniq = Counter(merged_data)
lemma_pos_uniq=Counter(lemma_pos)


lemma_file_count = Counter(file_data_lemma)
train_file_count = Counter(file_data_train)

pos_iob = []
for i in merged_data:
    pos_iob.append((i[2], i[3]))
pos_iob_uniq = Counter(pos_iob)


#############################          CREATE THE LEXICON            ###################################################
lexicon = open("lexicon_lemmatization.txt", "w")
counter_lexicon = 0
lexicon.write("<eps>"+"\t"+str(counter_lexicon)+"\n")
for i in words_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
for i in lemmas_uniq:
    if i not in words_uniq:
        counter_lexicon +=1
        lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
for i in iob_tags_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
for i in pos_tags_uniq:
    counter_lexicon +=1
    lexicon.write(i + "\t"+str(counter_lexicon)+"\n")
counter_lexicon += 1
lexicon.write("<unk>"+"\t"+str(counter_lexicon))
lexicon.close()


#############################         FIRST AUTOMATA: WORD-LEMMA       #################################################

#compute probilities/costs for the automata
probs_word_lemma = []
for i in words_uniq:
    for y in word_lemma_uniq:
        if i == y[0]:
            prob = word_lemma_uniq[y]/words_uniq[y[0]]
            if prob !=1 :
                probs_word_lemma.append((y[0], y[1], -(math.log(prob))))
            else:
                probs_word_lemma.append((y[0], y[1], 0))

#automata
automata1 = open("automata_1.txt", "w")
for i in probs_word_lemma:
    automata1.write("0" + "\t" + "0" + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
    automata1.write("\n")
for i in lemmas_uniq:
    if i not in words_uniq:
        automata1.write("0" + "\t" + "0" + "\t" + i + "\t" + i + "\t" + str(0))
        automata1.write("\n")

automata1.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + "<unk>"+ "\t" + str(0))

automata1.write("\n")
automata1.write("0")

#########################       SECOND AUTOMATA: LEMMA - POS   ##################################################

probs_lemma_pos = []

for x in pos_tags_uniq:
    for i in lemma_pos_uniq:
        if x == i[1]:
            prob = lemma_pos_uniq[i]/pos_tags_uniq[x]
            if prob !=1:
                probs_lemma_pos.append((i[0], i[1], -(math.log(prob))))
            else:
                probs_lemma_pos.append((i[0], i[1], 100))


#automata
automata2 = open("automata_2.txt", "w")
for i in probs_lemma_pos:
    automata2.write("0" + "\t" + "0" + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
    automata2.write("\n")

for i in pos_tags_uniq:
    automata2.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + i + "\t" + str(-math.log(1/pos_tags_uniq.__len__())))
    automata2.write("\n")

automata2.write("0")

############################## THIRD AUTOMATA: POS  - IOB    ######################################################

probs_pos_iob = []
for x in iob_tags_uniq:
    for i in pos_iob_uniq:
        if x == i[1]:
            prob = pos_iob_uniq[i]/iob_tags_uniq[i[1]]
            if prob !=1:
                probs_pos_iob.append((i[0], i[1], -math.log(prob)))
            else:
                probs_pos_iob.append((i[0], i[1], 100))


#automata
automata3 = open("automata_3.txt", "w")
for i in probs_pos_iob:
    automata3.write("0" + "\t" + "0" + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
    automata3.write("\n")

for i in iob_tags_uniq:
    automata3.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + i + "\t" + str(-math.log(1/iob_tags_uniq.__len__())))
    automata3.write("\n")

automata3.write("0")