#! /usr/bin/python3

"""
@:param: NLSPARQL.train.feats.txt
@:param: NLSPARQL.train.data
@:param: NLSPARQL.test.feats.txt
@:param: NLSPARQL.test.data

OUTPUT

IOB_sentence.txt:       train sentences in IOB tags format
words_sentence.txt:     test sentences, one sentence per line
lemma_sentence.txt:     test sentences in lemma format, one sentence per line
pos_sentence.txt:       test sentences in pos_tag format, one sentence per line
lexicon_word.txt:       lexicon for the first automa, transitions word - IOB tag
lexicon_lemma.txt:      lexicon for the second automa, transitions lemma - IOB tag
lexicon_pos.txt:        lexicon for the third automa, transitions pos tag - IOB tag
automata_1.txt:         automa transitions word - IOB tag
automata_2.txt:         automa transitions lemma - IOB tag
automata_3.txt:         automa transitions pos tag - IOB tag

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

file_data_lemma = []
file_data_train = []

#file in which sentence-of-tag are saved
IOB_sentence = open("IOB_sentence.txt","w")
#file that contains all the sentencenses without the tag
sentences=open("words_sentences.txt","w")
lemma_sentences=open("lemma_senteces.txt", "w")
pos_sentences=open("pos_sentences.txt","w")

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

#create the test input file for the second and third automata
with open(test_feats, "r") as f:
    tmp=f.read().split('\n')
    for line in tmp:
        if line !='':
            x, y, z = line.split('\t')
            lemma_sentences.write(z+" ")
            pos_sentences.write(y+" ")
        else:
            lemma_sentences.write('\n')
            pos_sentences.write('\n')



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

lemma_iob = []
for i in merged_data:
    lemma_iob.append((i[1], i[3]))
lemma_iob_uniq = Counter(lemma_iob)

#############################          CREATE THE LEXICON  FOR THE FIRST AUTOMA          ###############################
#this automa consider only the couple word - iob tags

lexicon = open("lexicon_word.txt", "w")
counter_lexicon = 0
lexicon.write("<eps>"+"\t"+str(counter_lexicon)+"\n")


for i in words_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
for i in iob_tags_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
counter_lexicon += 1
lexicon.write("<unk>"+"\t"+str(counter_lexicon))
lexicon.close()
#############################          CREATE THE LEXICON  FOR SECOND AUTOMA          ###############################
#this automa consider only the couple lemma - iob tags

lexicon = open("lexicon_lemma.txt", "w")
counter_lexicon = 0
lexicon.write("<eps>"+"\t"+str(counter_lexicon)+"\n")
for i in lemmas_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
for i in iob_tags_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
counter_lexicon += 1
lexicon.write("<unk>"+"\t"+str(counter_lexicon))
lexicon.close()

#############################          CREATE THE LEXICON  FOR THIRD AUTOMA          ###############################
#this automa consider only the couple pos - iob tags

lexicon = open("lexicon_pos.txt", "w")
counter_lexicon = 0
lexicon.write("<eps>"+"\t"+str(counter_lexicon)+"\n")
for i in pos_tags_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
for i in iob_tags_uniq:
    counter_lexicon +=1
    lexicon.write(i+"\t"+str(counter_lexicon)+"\n")
counter_lexicon += 1
lexicon.write("<unk>"+"\t"+str(counter_lexicon))
lexicon.close()


#############################         FIRST AUTOMATA: WORD - IOB      #################################################

#compute probilities/costs for the automata
probs_word_iob = []
for i in iob_tags_uniq:
    for y in train_file_count:
        if i == y[1]:
            prob = train_file_count[y]/iob_tags_uniq[i]
            if prob !=1 :
                probs_word_iob.append((y[0], y[1], -(math.log(prob))))
            else:
                probs_word_iob.append((y[0], y[1], 0.0))

#automata
automata1 = open("automata_1.txt", "w")
for i in probs_word_iob:
    automata1.write("0" + "\t" + "0" + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
    automata1.write("\n")
for i in iob_tags_uniq:
    automata1.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + i + "\t" + str(-math.log(1/iob_tags_uniq.__len__())))
    automata1.write("\n")

automata1.write("0")

#########################       SECOND AUTOMATA: LEMMA - IOB   ##################################################
conta_prova = 0

probs_lemma_iob = []
for i in iob_tags_uniq:
    for x in lemma_iob_uniq:
        if x[1] == i:
            prob = lemma_iob_uniq[x]/iob_tags_uniq[x[1]]
            if prob !=1:
                probs_lemma_iob.append((x[0], x[1], -math.log(prob)))
            else:
                probs_lemma_iob.append((x[0], x[1], 0.0))


#automata
automata2 = open("automata_2.txt", "w")
for i in probs_lemma_iob:
    automata2.write("0" + "\t" + "0" + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
    automata2.write("\n")

for i in iob_tags_uniq:
    automata2.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + i + "\t" + str(-math.log(1/iob_tags_uniq.__len__())))
    automata2.write("\n")

automata2.write("0")

# ############################## THIRD AUTOMATA: POS - IOB    ######################################################

probs_pos_iob = []
for i in iob_tags_uniq:
    for x in pos_iob_uniq:
        if x[1] == i:
            prob = pos_iob_uniq[x]/iob_tags_uniq[x[1]]
            if prob !=1:
                probs_pos_iob.append((x[0], x[1], -math.log(prob)))
            else:
                probs_pos_iob.append((x[0], x[1], 0.0))

#automata
automata3 = open("automata_3.txt", "w")
for i in probs_pos_iob:
    automata3.write("0" + "\t" + "0" + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
    automata3.write("\n")

for i in iob_tags_uniq:
    automata3.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + i + "\t" + str(-math.log(1/iob_tags_uniq.__len__())))
    automata3.write("\n")

automata3.write("0")


