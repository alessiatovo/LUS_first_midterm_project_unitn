#! /usr/bin/python3
""""
INSTRUCTIONS:

@:param: NLSPARQL.train.data
@:param: NLSPARQL.test.data
@:param: frequency minimun cut-off. Ex. 10 if you want consider only couple with frequency GREATER THAN 10
@:param: frequency maximum cut-off. Ex 400 if you want consider only couple with frequency LESS THAN 400

OUPTUT:

tag_sentence.txt:       train file sentences written in IOB tags format
sentences.txt:          test sentences, one sentence per line
word_info.txt:          occurencies of all the words contained in the train file
tags_info.txt:          occurencies of all the IOB tags contained in the train file and their prior probabilities
word_tag_info.txt:      occurencies of all the couples word - IOB_tag in the train file and their probabilites
lexicon_lower.txt:      lexicon for the lower cut-off case
lexicon_upper.txt:      lexicon for the upper cut-off case
automata_lower.txt:     automa for the lower cut-off case
automata_upper.txt:     automa for the upper cut-off case

"""

import sys
import math
from collections import Counter
from operator import itemgetter

input_file = sys.argv[1]
#read the test file to create a file of sentences without tags
input_test = sys.argv[2]
file_data = []
#file in which sentence-of-tag are saved
tag_sentence = open("IOB_sentence.txt","w")
#file that contains all the sentencenses without the tag
sentences=open("sentences.txt","w")
words=[]
tags_lower={}
tags_upper={}
with open(input_file, "r") as f:
    tmp = f.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            tag_sentence.write(y+" ")
            file_data.append((x,y))
            words.append(x)
            tags_lower[y]=0
            tags_upper[y]=0
        else:
            tag_sentence.write("\n")

tag_sentence.close()
with open(input_test, "r") as t:
    tmp = t.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            sentences.write(x + " ")
        else:
            sentences.write("\n")

words_count=Counter(words)
words_count.most_common()
words_file = open("words_info.txt", "w")

for i in words_count:
    words_file.write(str(i)+" "+str(words_count[i])+"\n")
words_file.close()
sentences.close()


#COUNT OCCURENCIES OF EACH COUPLE
counted_couple = Counter(file_data)

#COUNT THE OCCURENCIES FOR EACH TAG
labels=[]
for t in file_data:
    labels.append(t[1])
counted_labels = Counter(labels)

total_tags=0
for i in counted_labels:
    total_tags += counted_labels[i]

probs_tag = []
count_tag_file=open("tags_info.txt","w")
for x in counted_labels:
    probs_tag.append((str(x), -(math.log(counted_labels[x]/file_data.__len__())), str(counted_labels[x])))
    #count_tag_file.write(x+"\t\t"+str(counted_labels[x])+"\t\t"+str(-(math.log(counted_labels[x]/file_data.__len__())))+"\n")

#sort by frequency, descendent order
probs_tag.sort(key=lambda x: x[2], reverse=True)

#write in a document info about tags
for x in probs_tag:
    count_tag_file.write(x[0] + "\t\t" + str(x[1])+ "\t\t" + str(x[2]) + "\n")
count_tag_file.close()

#COMPUTE THE PROBABILITIES
probs = []
for x in counted_labels:
    for y in counted_couple:
        if x == y[1]:
            probs.append((y[0], y[1], -(math.log(counted_couple[y]/counted_labels[x])), counted_couple[y]))

#sort by frequency, descendent order
probs.sort(key=lambda x: x[3], reverse=True)



#write in a document info about the couples words-tags
word_tag_file=open("word_tag_info.txt","w")
for y in probs:
    word_tag_file.write(y[0] + "\t\t" + y[1] + "\t\t" + str(y[2]) + "\t\t" + str(y[3]) + "\n")
word_tag_file.close()

file_data = list(set(file_data))
file_data.sort()

########################################################################################
#cut off for words - LOWER BOUND

lexicon_lower=open("lexicon_lower.txt", "w")
count_lex=0
lexicon_lower.write("<eps>"+"\t"+str(count_lex)+"\n")
freq_min=int(sys.argv[3])
words_lower = []
couple_lower = []
for i in counted_couple:
    if words_count[i[0]] >= freq_min:
        words_lower.append(i[0])
        couple_lower.append((i[0], i[1], counted_couple[i]))
    else:
        tags_lower[i[1]] = tags_lower[i[1]]+counted_couple[i]


words_lower=list(set(words_lower))

#wirte into the lexicon file
for i in words_lower:
    count_lex += 1
    lexicon_lower.write(i+"\t"+str(count_lex)+"\n")
count_lex +=1
for k,v in tags_lower.items():
    lexicon_lower.write(str(k)+"\t"+str(count_lex)+"\n")
    count_lex +=1
lexicon_lower.write("<unk>"+"\t"+str(count_lex))

probs_lower = []
for i in couple_lower:
    remains= counted_labels[i[1]]-tags_lower[i[1]]
    if remains == 0:
        probs_lower.append((i[0], i[1], 0))
    else:
        probs_lower.append((i[0], i[1], -(math.log(i[2]/remains))))

######################################################################################
#cut off for words - UPPER BOUND

lexicon_upper=open("lexicon_upper.txt", "w")
count_lex=0
lexicon_upper.write("<eps>"+"\t"+str(count_lex)+"\n")
freq_max=int(sys.argv[4])
words_upper = []
couple_upper = []
for i in counted_couple:
    if words_count[i[0]] <= freq_max:
        words_upper.append(i[0])
        couple_upper.append((i[0], i[1], counted_couple[i]))
    else:
        tags_upper[i[1]] = tags_upper[i[1]]+counted_couple[i]


words_upper=list(set(words_upper))

#write into the lexicon file
for i in words_upper:
    count_lex += 1
    lexicon_upper.write(i+"\t"+str(count_lex)+"\n")
count_lex +=1
for k,v in tags_upper.items():
    lexicon_upper.write(str(k)+"\t"+str(count_lex)+"\n")
    count_lex +=1
lexicon_upper.write("<unk>"+"\t"+str(count_lex))

probs_upper = []
for i in couple_upper:
    remains= counted_labels[i[1]]-tags_upper[i[1]]
    if remains == 0:
        probs_upper.append((i[0], i[1], 0))
    else:
        probs_upper.append((i[0], i[1], -(math.log(i[2]/remains))))

######################################################################################

#create the first automata complete (without cut-off system)
# output_file = "automata_complete.txt"
#
# file_data_out=[]
#
# with open(output_file, "w") as o:
#     for x in probs:
#         file_data_out = o.write("0" +"\t"+ "0" +"\t"+str(x[0]) + "\t" +str(x[1])+"\t"+str(x[2]))
#         file_data_out=o.write("\n")
#     for x in counted_labels:
#         file_data_out = o.write("0"+"\t"+"0"+"\t"+"<unk>"+"\t"+str(x)+"\t"+str(-math.log(1/counted_labels.__len__())))
#         file_data_out = o.write("\n")
#     file_data_out = o.write("0")
#
# #create the automata that compute the priori probability of tags
# output_file_2 = "automata_priori_complete.txt"
# file_data_out_2 = []
# with open(output_file_2, "w") as o:
#     for x in probs_tag:
#         file_data_out = o.write("0" +"\t"+ "0" +"\t"+str(x[0]) + "\t" +str(x[0])+"\t"+str(x[1]))
#         file_data_out=o.write("\n")
#     file_data_out_2 = o.write("0")
#
# tag_sentence.close()

########################################################################################À

#automata with lower bound
automata_lower=open("automata_lower.txt","w")
for x in probs_lower:
    automata_lower.write("0" + "\t" + "0" + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    automata_lower.write("\n")
total_delete = sum(value for key, value in tags_lower.items())
diff_total=total_tags-total_delete
for key, value in tags_lower.items():
    diff_tag= counted_labels[key] - value
    if diff_tag != 0:
        automata_lower.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + str(key) + "\t" + str(-math.log(diff_tag / diff_total)))
        automata_lower.write("\n")
automata_lower.write("0")

#automata with upper bound
automata_upper=open("automata_upper.txt","w")
for x in probs_upper:
    automata_upper.write("0" + "\t" + "0" + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    automata_upper.write("\n")
total_delete = sum(value for key, value in tags_upper.items())
diff_total=total_tags-total_delete
for key, value in tags_upper.items():
    diff_tag= counted_labels[key] - value
    if diff_tag != 0:
        automata_upper.write("0" + "\t" + "0" + "\t" + "<unk>" + "\t" + str(key) + "\t" + str(-math.log(diff_tag / diff_total)))
        automata_upper.write("\n")
automata_upper.write("0")

