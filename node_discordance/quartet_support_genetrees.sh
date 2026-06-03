#!/bin/bash

while getopts i:s:a: flag; do
  case "${flag}" in
    i) argI=${OPTARG} ;;  #-i = gene trees file 
    s) argS=${OPTARG} ;; #-s = species tree
    a) argA=${OPTARG} ;; #-a = path/to/astral.5.7.8
  esac
done

#create the star tree
python node_discordance/star_tree.py -t $argS -o output/tmp/star_tree.tre

#create a file with species trees nodes scored for each gene trees
cat $argI | while IFS= read line
do
	echo $line > output/tmp/genetree.tre   #overwrite
	cat output/tmp/star_tree.tre >> output/tmp/genetree.tre  #add to the file
	java -jar $argA -i output/tmp/genetree.tre -q $argS -t8 >> output/tmp/scored_genetree.tre
done 

rm output/tmp/genetree.tre

##store quartet supports in a dataframe
python node_discordance/quartet_dataframe.py -t output/tmp/scored_genetree.tre -o output/genetrees_quartet_support.csv


