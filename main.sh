#!/bin/bash

start=$SECONDS

while getopts i:s:a: flag; do
  case "${flag}" in
    i) argI=${OPTARG} ;;  #-i = input gene trees file 
    s) argS=${OPTARG} ;;  #-s = species tree newick 
    a) argA=${OPTARG} ;; #-a path/to/astral.5.7.8
  esac
done

#get quartet supports with Astral
##annotate the species tree
echo "Scoring the species tree with quartet supports."

java -jar $argA -i $argI -q $argS -t 2 -o output/tmp/ASTRAL_speciestree_ANNOTATED.tre 2> output/tmp/log_astral_annotated.log

##write annotations in a .csv + number the species tree nodes
echo "Extracting quartet support."

python species_tree/quartet_support/get_annotations.py -t output/tmp/ASTRAL_speciestree_ANNOTATED.tre -o output/tmp/quartet_support.csv 

##add a D stat column to the .csv
echo "Calculating the D statistics."

Rscript species_tree/quartet_support/D_stat.R -i output/tmp/quartet_support.csv -o output/quartet_support_Dstat.csv

##Number the species tree
echo "Numbering the species tree nodes"

python species_tree/quartet_support/number_speciestree.py -s $argS -o output/speciestree_NUMBERED.tre


#get branch lengths with Erable
##unroot the initial species tree + change taxon names for phylip format
echo "Converting in phylip format for erable."

python species_tree/scaled_gene_trees/change_species_name_for_phylip.py -t $argS -o output/tmp/ASTRAL_speciestree_UNROOTED.tre

##get distance matrix from gene trees
echo "Extracting the distance matrix."

python species_tree/scaled_gene_trees/get_dist_matrix.py -t $argI -o output/tmp/distance_matrix.txt

##run erable
echo "Running erable."

erable -i output/tmp/distance_matrix.txt -t output/tmp/ASTRAL_speciestree_UNROOTED.tre

##scale the gene trees with erable rates
###clean erable rates file
Rscript species_tree/scaled_gene_trees/clean_matrix.R -i output/tmp/distance_matrix.txt.rates.txt -o output/tmp/distance_matrix.txt.ratesCLEANED.txt

###scale 
echo "Scaling the gene trees with erable rates."

python species_tree/scaled_gene_trees/scale_branches_by_rates.py -t $argI -r output/tmp/distance_matrix.txt.ratesCLEANED.txt -o output/gene_trees_SCALED.treefile

#score each node of the species tree for all gene trees
echo "Getting quartet support for each species tree node for all gene trees."

bash node_discordance/quartet_support_genetrees.sh -i $argI -s $argS -a $argA

#create a csv file with D (discordant), C (concordant) or N (Not determined) for each node of the species tree for each gene tree.
echo "Getting discordance or concordance for each node."

python node_discordance/discordance_dataframe.py -i output/genetrees_quartet_support.csv -o output/discordance_dataframe.csv

#get a csv file with the height of each node of each gene tree corresponding to a node in the species tree.
echo "Getting the height of each node"

python correspondence/correspondence.py -t output/gene_trees_SCALED.treefile -s $argS -d output/discordance_dataframe.csv -o output/height_dataframe.csv

#final results table
echo "Creating a table with final results"

Rscript compute_H_index.R -c output/discordance_dataframe.csv -l output/height_dataframe.csv -d output/quartet_support_Dstat.csv -o output/final_results.csv

duration=$(( SECONDS - start ))
echo "Total running time:" $duration "seconds"
