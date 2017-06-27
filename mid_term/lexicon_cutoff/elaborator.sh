#! /bin/bash

#this script does:	farcompilestrings to generate the data.far necessary to apply the ngram commands
#					for each sentence compute the IOB-tags. 
#					@param1 : automata_file.fst
#					@param2 : lexicon_file.txt
#					@param3 : test sentence file .txt (ex: sentences.txt)
#					@param4 : --order (ex: 3)
#					@param5 : --method	(ex: witten_bell)
#sentence.txt		-> file made through main_script.sh (static name). Contains all the sentences of NLSPARQL.test.data in line format
#output_file.txt 	-> contains the outputs of fstprint command for each line, seperated by an empty line
#final.txt 			-> 	output file which contains: word	test_tag	train_tag	cost
#						this file is used to do the evaluation
#evaluation*.txt 	-> 	contains all the evaluation metrics		
	
#BEFORE EXECUTE THIS SCRIPT DELETE THE FILE output_file.txt IN THE DIRECTORY, IF IT EXISTS


doc=$3
counter=0
mkdir $5
output_file='output_file_'$4'_'$5'.txt'
> $5/$output_file

#doc2='prova.txt'
farcompilestrings --symbols=$2 --unknown_symbol='<unk>' IOB_sentence.txt > data.far
while IFS= read -r line; do
	ngramcount --order=$4 --require_symbols=false data.far > pos.cnt
	ngrammake --method=$5 pos.cnt > pos.lm
	echo "$line" | farcompilestrings --symbols=$2 --unknown_symbol='<unk>' --generate_keys=1 --keep_symbols | farextract --filename_suffix='.fst'
	fstcompose 1.fst $1 | fstcompose - pos.lm | fstrmepsilon | fstshortestpath | fsttopsort | fstprint --isymbols=$2 --osymbols=$2 >> $5/$output_file 
	((counter++))
	echo " " >> $5/$output_file
  	echo "line $counter: $line"
done < $doc 

awk '{print $4}' < $5/$output_file | awk -v RS= -v ORS='\n\n' '1' > tmp.txt
paste NLSPARQL.test.data tmp.txt > $5/final_$5_$4.txt
#file that contains all the evaluation measures 
perl conlleval.pl -d "\t" < $5/final_$5_$4.txt > $5/evaluation_$4.txt

rm data.far pos.cnt pos.lm 1.fst tmp.txt $5/final_$5_$4.txt $5/$output_file