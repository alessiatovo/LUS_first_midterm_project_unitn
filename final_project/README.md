README

This document has the purpose to exaplain how compile correctly the final_project.

Inside the directory final_project there are two sub directories: crf and rnn.

-------------------------------------------------------------------------------------

CRF INSTRUCTIONS

In order to execute following scripts you have to install correctly CRF ++ tool.

The script merge.py crete a new test set and a new train set, merging the two orignal ones. This script require a number parameter that is the lenght of prefix and suffix. These documents will be created in the data folder.

In order to execute the best template that gives best performances run the script ./script.sh. This script also executes the ./merge.py script, since the template uses additional features. The parameter near the script is necessary in order to create prefix and suffix features. In the script is setted to 3 which gives s better performance than other values.

In the console you can see the performance of CRF model which should correspond to the one written in the report document.

-----------------------------------------------------------------------------------

RNN INSTRUCTION

This code is given during the course and is based on papers:

[Grégoire Mesnil, Xiaodong He, Li Deng and Yoshua Bengio - **Investigation of Recurrent Neural Network Architectures and Learning Methods for Spoken Language Understanding**](http://www.iro.umontreal.ca/~lisa/pointeurs/RNNSpokenLanguage2013.pdf)

[Grégoire Mesnil, Yann Dauphin, Kaisheng Yao, Yoshua Bengio, Li Deng, Dilek Hakkani-Tur, Xiaodong He, Larry Heck, Gokhan Tur, Dong Yu and Geoffrey Zweig - **Using Recurrent Neural Networks for Slot Filling in Spoken Language Understanding**](http://www.iro.umontreal.ca/~lisa/pointeurs/taslp_RNNSLU_final_doubleColumn.pdf)

## Code

In order to reproduce the results, make sure Theano is installed and the
repository is in your `PYTHONPATH`, e.g run the command

`export PYTHONPATH=/path/where/rnn_slu/is:$PYTHONPATH`.

Script ./script.py is foundamental to generate documents necessary to build the RNN model, like word lexicon document, label lexicon document, validation and train set.

(Following scripts may take long time, like ~ 40 minutes)

Script ./launch_elman.sh allow to exectue the Elman model that gives best results. The result are visible in console. 

Script ./launch_jordan.sh allow to exectue the Elman model that gives best results. The result are visible in console. 

