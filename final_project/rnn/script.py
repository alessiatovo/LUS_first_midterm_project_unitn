#! /usr/bin/python3

import sys
from collections import Counter
import random

Seed = 793
random.seed(Seed)

word_lexicon = open ("rnn_slu/data/word_lexicon.txt", "w")
label_lexicon = open ("rnn_slu/data/label_lexicon.txt", "w")

#file lex with lemma concatenation--------------------------------
word_lexicon_lemma =open("rnn_slu/data/lemma/word_lexicon_lemma.txt", "w")
label_lexicon_lemma = open("rnn_slu/data/lemma/label_lexicon_lemma.txt", "w")

#file lex with pos concatenation--------------------------------
word_lexicon_pos =open("rnn_slu/data/pos/word_lexicon_pos.txt", "w")
label_lexicon_pos = open("rnn_slu/data/pos/label_lexicon_pos.txt", "w")

#file lex with lemma_pos concatenation--------------------------------
word_lexicon__lemma_pos =open("rnn_slu/data/lemma_pos/word_lex_lp.txt", "w")
label_lexicon_lemma_pos = open("rnn_slu/data/lemma_pos/label_lex_lp.txt", "w")

#file lex with word_lemma_pos concatenation--------------------------------
word_lexicon_wlp =open("rnn_slu/data/word_lemma_pos/word_lexicon_wlp.txt", "w")
label_lexicon_wlp = open("rnn_slu/data/word_lemma_pos/label_lexicon_wlp.txt", "w")


#-------------------------------------------------------------

words = []
labels = []
sentences = []
line = []
tmp = open ("rnn_slu/data/train.txt", "w")
tmp2 = open ("rnn_slu/data/validation.txt", "w")

#file with word_lemma concatenation------------------------------
train_lemma_file = open("rnn_slu/data/lemma/train.txt", "w")
validation_lemma_file = open("rnn_slu/data/lemma/validation.txt", "w")
test_lemma = open("rnn_slu/data/lemma/test.txt", "w")

words_lemma = []
sentences_lemma = []
line_lemma = []

#file with word_pos concatenation----------------------------------
train_pos_file = open("rnn_slu/data/pos/train.txt", "w")
validation_pos_file = open("rnn_slu/data/pos/validation.txt", "w")
test_pos = open("rnn_slu/data/pos/test.txt", "w")

words_pos = []
sentences_pos = []
line_pos = []

#file with lemma_pos concatenation----------------------------------
train_lemmapos_file = open("rnn_slu/data/lemma_pos/train.txt", "w")
validation_lemmapos_file = open("rnn_slu/data/lemma_pos/validation.txt", "w")
test_lemmapos = open("rnn_slu/data/lemma_pos/test.txt", "w")

words_lemma_pos = []
sentences_lemma_pos = []
line_lemma_pos = []

#file with word_lemma_pos concatenation----------------------------------
train_wlp_file = open("rnn_slu/data/word_lemma_pos/train.txt", "w")
validation_wlp_file = open("rnn_slu/data/word_lemma_pos/validation.txt", "w")
test_wlp = open("rnn_slu/data/word_lemma_pos/test.txt", "w")

words_wlp = []
sentences_wlp = []
line_wlp = []
#----------------------------------------------------------------

with open("rnn_slu/data/NLSPARQL.train.data", "r") as d,open("rnn_slu/data/NLSPARQL.train.feats.txt", "r") as f:
    tmp_d = d.read().split('\n')
    tmp_f = f.read().split('\n')
    for line_data, line_feats in zip(tmp_d, tmp_f):
        if line_data !='' and line_feats!='':
            word,iob = line_data.split('\t')
            c, pos, lemma = line_feats.split('\t')
            new_word = word +"_"+lemma
            word_pos=word+"_"+pos
            word_lemmapos= lemma+"_"+pos
            word_wlp=word+"_"+lemma+"_"+pos
            words.append(word)
            labels.append(iob)
            line.append((word, iob))
            words_lemma.append(new_word)
            line_lemma.append((new_word, iob))
            words_pos.append(word_pos)
            words_wlp.append(word_wlp)
            line_pos.append((word_pos, iob))
            words_lemma_pos.append(word_lemmapos)
            line_lemma_pos.append((word_lemmapos, iob))
            line_wlp.append((word_wlp, iob))


        else:
            if len(line) != 0 and len(line_lemma) !=0:
                sentences.append(line)
                sentences_lemma.append(line_lemma)
                sentences_pos.append(line_pos)
                sentences_lemma_pos.append(line_lemma_pos)
                sentences_wlp.append(line_wlp)
            #tmp.write(str(line)+ "\n")
            line = []
            line_lemma = []
            line_pos=[]
            line_lemma_pos = []
            line_wlp=[]

with open("rnn_slu/data/NLSPARQL.test.data", "r") as d, open("rnn_slu/data/NLSPARQL.test.feats.txt", "r") as f:
    tmp_d = d.read().split('\n')
    tmp_f = f.read().split('\n')
    for line_data, line_feats in zip(tmp_d, tmp_f):
        if line_data !='' and line_feats!='':
            word,iob = line_data.split('\t')
            c, pos, lemma = line_feats.split('\t')
            new_word=word+"_"+lemma
            word_pos = word+"_"+pos
            word_lemmapos=lemma+"_"+pos
            word_wlp=word+"_"+lemma+"_"+pos
            test_lemma.write(new_word+" "+iob+"\n")
            test_pos.write(word_pos+" "+iob+"\n")
            test_lemmapos.write(word_lemmapos+" "+iob+"\n")
            test_wlp.write(word_wlp+" "+iob+"\n")
            labels.append(iob)
        else:
            test_lemma.write("\n")
            test_pos.write("\n")
            test_lemmapos.write("\n")
            test_wlp.write("\n")


#create validation and test data with input parameters for the percentage ######################################


random.shuffle(sentences)

perc = int(sys.argv[1])
#perc = int(10)
val_len = int(len(sentences)*perc/100)
train_len = int(len(sentences)-val_len)

#standard train

validation = sentences[:val_len]
train = sentences[val_len:]

for i in validation:
    for j in i:
        tmp2.write(str(j[0]) +" "+str(j[1])+"\n")
    tmp2.write("\n")

for i in train:
    for j in i:
        tmp.write(str(j[0]) + " " + str(j[1]) + "\n")
    tmp.write("\n")


#word_lemma train -----------------------------------------------------
random.shuffle(sentences_lemma)

val_lemma = sentences_lemma[:val_len]
train_lemma = sentences_lemma[val_len:]

for i in val_lemma:
    for j in i:
        validation_lemma_file.write(str(j[0]) +" "+str(j[1])+"\n")
    validation_lemma_file.write("\n")

for i in train_lemma:
    for j in i:
        train_lemma_file.write(str(j[0]) + " " + str(j[1]) + "\n")
    train_lemma_file.write("\n")

# word_pos train--------------------------------------------------------

random.shuffle(sentences_pos)

val_pos = sentences_pos[:val_len]
train_pos = sentences_pos[val_len:]

for i in val_pos:
    for j in i:
        validation_pos_file.write(str(j[0]) + " " + str(j[1]) + "\n")
    validation_pos_file.write("\n")

for i in train_pos:
    for j in i:
        train_pos_file.write(str(j[0]) + " " + str(j[1]) + "\n")
    train_pos_file.write("\n")

# lemma_pos train--------------------------------------------------------

random.shuffle(sentences_lemma_pos)

val_lemma_pos = sentences_lemma_pos[:val_len]
train_lemma_pos = sentences_lemma_pos[val_len:]

for i in val_lemma_pos:
    for j in i:
        validation_lemmapos_file.write(str(j[0]) + " " + str(j[1]) + "\n")
    validation_lemmapos_file.write("\n")

for i in train_lemma_pos:
    for j in i:
        train_lemmapos_file.write(str(j[0]) + " " + str(j[1]) + "\n")
    train_lemmapos_file.write("\n")

# word_lemma_pos train--------------------------------------------------------

random.shuffle(sentences_lemma_pos)

val_wlp = sentences_wlp[:val_len]
train_wlp = sentences_wlp[val_len:]

for i in val_wlp:
    for j in i:
        validation_wlp_file.write(str(j[0]) + " " + str(j[1]) + "\n")
    validation_wlp_file.write("\n")

for i in train_wlp:
    for j in i:
        train_wlp_file.write(str(j[0]) + " " + str(j[1]) + "\n")
    train_wlp_file.write("\n")


# create lexicon files##############################################################################

#standard train
words = set(words)
labels = set(labels)

count_lex = 0
for i in words:
    word_lexicon.write(i + "\t"+str(count_lex)+"\n")
    count_lex+=1
word_lexicon.write("<UNK>"+"\t"+str(count_lex)+"\n")

count_lex = 0
for i in labels:
    label_lexicon.write(i +"\t" + str(count_lex)+"\n")
    count_lex+=1

#word_lemma train-----------------------------------------------------

words_lemma = set(words_lemma)

count_lex = 0
for i in words_lemma:
    word_lexicon_lemma.write(i + "\t"+str(count_lex)+"\n")
    count_lex+=1
word_lexicon_lemma.write("<UNK>"+"\t"+str(count_lex)+"\n")

count_lex = 0
for i in labels:
    label_lexicon_lemma.write(i +"\t" + str(count_lex)+"\n")
    count_lex+=1

# word_pos train ------------------------------------------------------

words_pos = set(words_pos)

count_lex = 0
for i in words_pos:
    word_lexicon_pos.write(i + "\t" + str(count_lex) + "\n")
    count_lex += 1
word_lexicon_pos.write("<UNK>" + "\t" + str(count_lex) + "\n")

count_lex = 0
for i in labels:
    label_lexicon_pos.write(i + "\t" + str(count_lex) + "\n")
    count_lex += 1


# lemma_pos train ------------------------------------------------------

words_lemma_pos = set(words_lemma_pos)

count_lex = 0
for i in words_lemma_pos:
    word_lexicon__lemma_pos.write(i + "\t" + str(count_lex) + "\n")
    count_lex += 1
word_lexicon__lemma_pos.write("<UNK>" + "\t" + str(count_lex) + "\n")

count_lex = 0
for i in labels:
    label_lexicon_lemma_pos.write(i + "\t" + str(count_lex) + "\n")
    count_lex += 1

# word_lemma_pos train ------------------------------------------------------

words_wlp = set(words_wlp)

count_lex = 0
for i in words_wlp:
    word_lexicon_wlp.write(i + "\t" + str(count_lex) + "\n")
    count_lex += 1
word_lexicon_wlp.write("<UNK>" + "\t" + str(count_lex) + "\n")

count_lex = 0
for i in labels:
    label_lexicon_wlp.write(i + "\t" + str(count_lex) + "\n")
    count_lex += 1