README

This document has the aim to explain all the steps to compile correctly the project. More details about the project are written in the report.pdf

The are four different project implementations, each of them corresponds to a specific directory: independent_features, lexicon_cutoff, standard_training and lemmapos.
Each directory contains all the files necessary to do three different types of testing:
- standard_training: the main.py script generates three different automata_files (.txt extensions) to do standard training and testing, i.e. the transitions word/lemma/pos -> iob tag are used 
	1 - Automa for transitions word - iob tag
	2 - Automa for transitions lemma - iob tag
	3 - Automa for transition pos - iob tag.
	
- independent_features:	the ind_feat_script.py script generates three automata to compose. The idea of this train and test is to consider the triple word-lemma-pos independent in order to assign the iob tag to the input words.

- lexicon_cutoff: the main_script.py script generates two different automata, one for the upper bound case and the other for the lower bound case. The idea of this train and test is to delete from the automa all the words that have a certain frequency, greater o less than a certain value.

- lemmapos: main.py script crate an automa for the transition lemmapos - iob. The lemmapos is a word composed by the concatenation of lemma and pos tag of the train file.

The instructions needed to execute the scripts and doing the tests are explained in the following sections.

----------------------------------------------------------------------------------------------------------------------------

STANDARD TRAINING

Step 1:
./main.py NLSPARQL.train.feats.txt NLSPARQL.train.data NLSPARQL.test.feats.txt NLSPARQL.test.data

Step 2:
./compilation.sh

Step 3: 
#the only two paramter that is possible to change are:
 -  <order>:	put an integer number between 1 and 5
 -  <method>:	put one of these six smoothing method: absolute, witten_bell, kneser_ney, katz, unsmoothed, presmoothed

IN ORDER TO EXECUTE THIS STEP AND MAINTAIN ALL THE RESULTS, CREATE THREE DIFFERENT FOLDERS CALLED word_test, lemma_test AND pos_test AND COPY THE FOLLOWING FILES INTO THE DIRECTORIES BEFORE EXECUTING THE COMMAND.

Evaluation results are contained in the directory named <method>

A - The folder word_test must contain:
 	elaborator.sh
 	conlleval.pl
 	lexicon_word.txt
 	automata_1_sort.fst
 	IOB_sentence.txt
 	words_sentences.txt
 	NLSPARQL.test.data

 	Than it is possbile executed this command
	./elaborator.sh automata_1.fst lexicon_word.txt words_sentences.txt <order> <method>

B - The folder lemma_test must contain:
 	elaborator.sh
 	conlleval.pl
 	lexicon_lemma.txt
 	automata_2_sort.fst
 	IOB_sentence.txt
 	lemma_sentences.txt
 	NLSPARQL.test.data

 	Than it is possbile executed this command
	./elaborator.sh automata_2.fst lexicon_lemma.txt lemma_sentences.txt <order> <method>

C - The folder pos_test must contain:
 	elaborator.sh
 	conlleval.pl
 	lexicon_pos.txt
 	automata_3_sort.fst
 	IOB_sentence.txt
 	pos_sentences.txt
 	NLSPARQL.test.data

 	Than it is possbile executed this command
	./elaborator.sh automata_2.fst lexicon_pos.txt pos_sentences.txt <order> <method>


---------------------------------------------------------------------------------------------------------------------------

INDEPENDENT FEATURES 

Step 1:
./ind_feat_script.py  NLSPARQL.train.feats.txt NLSPARQL.train.data NLSPARQL.test.data

Step 2:
./compilation.sh

Step 3:
./elaborator.sh automata_complete.fst lexicon_lemmatization.txt sentences.txt <order> <method>
 
The only two paramter that is possible to change are:
 - <order>:	put an integer number between 1 and 5
 -  <method>:	put one of these six smoothing method: absolute, witten_bell, kneser_ney, katz, unsmoothed, presmoothed

Evaluation results are contained in the directory named <method>

----------------------------------------------------------------------------------------------------------------------------

LEXICON CUT-OFF

Step 1:
#choose a lower bound and an upper bound. All the words with frequency lower than <lower-bound> will be deleted and all the word with frequency more than <upper-bound> will be deleted.
./main_script.py NLSPARQL.train.data NLSPARQL.test.data <lower-bound> <upper-bound>

Step 2:
./compilation.sh

Step 3: 
#the only two paramter that is possible to change are:
 - 	<order>:	put an integer number between 1 and 5
 -  <method>:	put one of these six smoothing method: absolute, witten_bell, kneser_ney, katz, unsmoothed, presmoothed

IN ORDER TO EXECUTE THIS STEP AND MAINTAIN ALL THE RESULTS, CREATE TWO DIFFERENT FOLDERS CALLED lower_test AND upper_test and copy AND COPY THE FOLLOWING FILES INTO THE DIRECTORIES BEFORE EXECUTING THE COMMAND.
Evaluation results are contained in the directory named <method>.
  
The folder lower_test must contain:
 	elaborator.sh
 	conlleval.pl
 	lexicon_lower.txt
 	automata_lower.fst
 	IOB_sentence.txt
 	sentences.txt
 	NLSPARQL.test.data

 	Than it is possbile executed this command
	./elaborator.sh automata_lower.fst lexicon_lower.txt sentences.txt <order> <method>

The folder upper_test must contain:
 	elaborator.sh
 	conlleval.pl
 	lexicon_upper.txt
 	automata_upper.fst
 	IOB_sentence.txt
 	sentences.txt
 	NLSPARQL.test.data

 	Than it is possbile executed this command
	./elaborator.sh automata_upper.fst lexicon_upper.txt sentences.txt <order> <method>

----------------------------------------------------------------------------------------------------------------------------

LEMMAPOS

Step 1:
./mian.py  NLSPARQL.train.feats.txt NLSPARQL.train.data NLSPARQL.test.feats.txt NLSPARQL.test.data

Step 2:
./compilation.sh

Step 3: 
./elaborator.sh automata_complete.fst lexicon_lemmatization.txt sentences.txt <order> <method>

The only two paramter that is possible to change are:
 -  <order>:	put an integer number between 1 and 5
 -  <method>:	put one of these six smoothing method: absolute, witten_bell, kneser_ney, katz, unsmoothed, presmoothed
 
Evaluation results are contained in the directory named <method>
