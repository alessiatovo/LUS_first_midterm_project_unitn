#! /bin/bash

#create the transducer given the automata file .txt generated by main.py script

#no input line parameters required

fstcompile --isymbols=lexicon.txt --osymbols=lexicon.txt automa.txt > automa.fst
