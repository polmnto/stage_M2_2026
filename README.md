# Computing a Height Index that detects Gene Flow 

This pipeline aims at comparing two indexes of phylogenetic conflicts: the asymetry of discordant topologies (as in the D statistic) and the branch lengths/node height (as in QuIBL or Aphid).
It can be divided into three main steps: 

1) It will score a species tree with quartet supports to calculate a "D-statistic like" measure using Astral. Folder 'species_tree/quartet_support'.

2) It will also rescale all the gene trees to get more realistic branch lengths values (that does not depend on mutation rate variation) using Erable (Binet et al., 2016). Thoses values are used to scale the input gene trees. Folder 'species_tree/scaled_gene_trees'.
	
3) It will measure the height of each node of the species tree in every gene trees, resulting in a distribution of heights for each node of the species tree :

	3.1) For each node of the species tree, it will determine if each gene tree is either concordant, discordant 1 or discordant 2 (the two possible discordant topologies). Folder 'node_discordance'.
	
	3.2) It will perform a correspondence between each gene trees nodes and species tree nodes in order extract the height of each node of the species tree for each gene tree. This correspondence considers the concordance/discordance of the node (determined above) to take alternative topologies into account. Folder 'correspondence'.

Thus, it provides the necessary material to calculate a height index that allow to detect gene flow using gene trees data. A example of a script in R which compute this statistic and compare it with the D stat by generating a figure (H ~ D) is also provided ('compute_H_index.R').

## Dependencies

* Python (this program was made using the 3.13.11 version)
* pandas 
* Ete3 (https://etetoolkit.org/)
* Astral.5.7.8 (https://github.com/smirarab/ASTRAL/tree/master)
* Erable (http://www.atgc-montpellier.fr/erable/)
* R (here version 4.6.0 used)

## Run the pipeline

The command syntax is :

$ ./main.sh -i {input gene tree file} -s {species tree} -a {path/to/astral}

-i : a file where each line is a gene tree in the newick format. It is very important that the gene trees are ROOTED before performing this analysis. You might also want to clean your dataset before. For instance, trees with aberrant branch length values may interfere with the Erable scaling.

-s : a ROOTED species tree in the newick format. You might want to have accurate branch lengths for your further analysis even if only its topology is used here.

-a : the path to the Astral program, for example /home/darwin/Documents/Programs/Astral.5.7.8/Astral/astral.5.7.8.jar


## Outputs

IMPORTANT : the "final_results.csv" table is what you want to look at at the end. It contains the H index, the Dstat, the concordance factor (q1) for all nodes considered. It also shows the number of short discordant gene tree (nb_D_nodes_INF) and the total number of discordant gene trees (nb_D_nodes). The "discordance_rate" column is just 1-q1 so like a "discordance factor". A final figure file is also created consisting in the Dstat plotted against the H index (asymetry index VS height index). The size of the points are related to the discordance rate. The straight line is the mean H index expected under the null hypothesis, the dashed line is the 5% threshold of significance and the dotted line is the 1% threshold. All those threshold were computed using 1000 simulations of datasets in absence of gene flow (i.e. the null hypothesis).

ASTRAL_speciestree.tre : the species tree inferred by Astral. Note that it is mostly relevant for the topology.

ASTRAL_speciestree_NUMBERED.tre : the same tree but with numbered nodes. It might be useful for intepretation and can be visualised using Dendroscope for example.

gene_trees_SCALED.treefile : a file containing all the input gene trees but scaled thanks to Erable. 

genetrees_quartet_support.csv : a table with the quartet support frequencies for each toplogy for each nodes of the species tree for each gene tree. In the example 0.8|0.1|0.1, the first number is q1 (the concordant topology and the second and third are q2 and q3 (quartet support frequencies for the alternative topologies).

The three main outputs are the following .csv files (they are used to compute the final_results table) :

- quartet_support_Dstat.csv : a table with quartet support for each node of the species tree and other measure corresponding to the Astral 'full annotation' when scoring a tree (https://github.com/smirarab/ASTRAL/blob/master/astral-tutorial.md#scoring-existing-trees). IMPORTANT : the last column is the D statistic equivalent calculated using the quartet support for alternative topologies.

D = (q2 - q3) / (q2 + q3) for each node of the species tree, where q2 and q3 are the quartet support frequencies for each alternative topology (i.e. ABBA and BABA).

- discordance_dataframe.csv : a table with C, D1, D2 or N for each node of the species tree for each gene tree. They are determined using the genetrees_quartet_support.csv file
	C : concordant node
	D1 : discordant node (q2 is the main quartet support)
	D2 : discordant node (q3 is the main quartet support)
	N : non determined node (ex: q1=0.5;q2=0.5:q3=0)
	
- height_dataframe.csv : a table with height of each node of the species tree for each gene tree. They are determined according the discordance/concordance state of the node (from the previous dataframe).

The tmp folder contains all the temporary files generated and used in the pipeline.

## Example

The 'input' folder contains gene trees, a species tree and a file with each node ages that you can use to test this analysis. The data comes from Vanderpool et al. (2020) but was cleaned and adapted. We removed all the gene trees without the outgroup 'Mus musculus' and we reduce the gene trees to the species of interest (all primates except Strepsirrhini and Tarsier).
