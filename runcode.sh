#!/bin/bash 
echo $1
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0100000000.txt $1
wait 
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0010000000.txt $1
wait
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0001000000.txt $1
wait
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0000100000.txt $1
wait 
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0000010000.txt $1
wait 
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0000001000.txt $1
wait 
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0000000100.txt $1
wait 
python correlations_two.py func 1 dumpfile.0000000000.txt dumpfile.0000000010.txt $1
wait 
