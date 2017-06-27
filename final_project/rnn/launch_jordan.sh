#! /bin/bash

python rnn_slu/lus/rnn_jordan_train.py rnn_slu/data/train.txt rnn_slu/data/validation.txt rnn_slu/data/word_lexicon.txt rnn_slu/data/label_lexicon.txt rnn_slu/config.cfg model_jordan
python rnn_slu/lus/rnn_jordan_test.py model_jordan rnn_slu/data/NLSPARQL.test.data rnn_slu/data/word_lexicon.txt rnn_slu/data/label_lexicon.txt rnn_slu/config.cfg test_jordan.txt


