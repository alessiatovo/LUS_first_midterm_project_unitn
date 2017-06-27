# !/bin/bash

./merge.py 3
crf_learn template/t_008 data/merged_train.txt model/model_008
crf_test -m model/model_008 data/merged_test.txt > output/output_008
perl conlleval.pl -d '\t' < output/output_01_compl > eval/eval_008
cat eval/eval_008
