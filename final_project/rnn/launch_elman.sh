#! /bin/bash

python rnn_slu/lus/rnn_elman_train.py rnn_slu/data/train.txt rnn_slu/data/validation.txt rnn_slu/data/word_lexicon.txt rnn_slu/data/label_lexicon.txt rnn_slu/config.cfg model_elman

python rnn_slu/lus/rnn_elman_test.py model_elman rnn_slu/data/NLSPARQL.test.data rnn_slu/data/word_lexicon.txt rnn_slu/data/label_lexicon.txt rnn_slu/config.cfg test_elman.txt 
	
