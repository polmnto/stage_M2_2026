from ete3 import Tree
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--treefile") #scaled gene trees
parser.add_argument("-s", "--speciestree") #Astral rooted species trees
parser.add_argument("-d", "--discordancetable")
parser.add_argument("-o", "--output")
args = parser.parse_args()

#FUNCTIONS:
##get relevant leaves
def relevant_leaves(node1, node2, tree):
    ls_under = []
    for leaf in node1.get_leaves():
        ls_under.append(leaf.name) 
    for leaf in node2.get_leaves():
        ls_under.append(leaf.name) 
    lg = []
    for leaf in tree.get_leaves():
        lg.append(leaf.name) 
    X = set(ls_under) & set(lg) 
    return(X)
    
def leaves_under_node(node, tree):
    ls_under = []
    for leaf in node.get_leaves():
        ls_under.append(leaf.name)  
    lg = []
    for leaf in tree.get_leaves():
        lg.append(leaf.name) 
    X = set(ls_under) & set(lg) 
    return(X)
    
##define genetree node support
def support(node, r_leaves):
    lg_under = []
    for leaf in node.get_leaves():  
        lg_under.append(leaf.name) #get all leaves under a given node in the given gene tree
    support = 2 * (len(set(r_leaves) & set(lg_under))) / (len(r_leaves) + len(lg_under)) #calculate the support
    return(support)

##get height of a node
def get_height(node):
    taxa = []
    for leaf in node.get_leaves():
        taxa.append(leaf.name)
    distance = []
    for i in taxa:
        d = node.get_distance(node&i) #calculate distance between the node and each of its leaves
        distance.append(d)
    h = sum(distance)/len(distance) #height = mean of the distance
    return(h)

## "is it an internal?" node function
def int_node(node):
	children = node.get_children()
	for i in children:
		if i.is_leaf() == False:
			return(i)

#SCRIPT
##import trees and discordance table
trees = []
for line in open(args.treefile):
    t = Tree(line)
    trees.append(t)
    
speciestree = Tree(args.speciestree)

disc = pd.read_csv(args.discordancetable, sep = "\t")

##create dataframe
column1 = []
n = 2

first_int_node = int_node(speciestree)

for node in speciestree.traverse():
    if node.is_leaf() == False and node.is_root() == False and node != first_int_node:
        column1.append(n)
        n += 1

data = {'node': column1}
df = pd.DataFrame(data)

##correspondence
row_count = 0  # = species tree node number index
col_count = 1  # = gene number

height = [] #list of heights of nodes of the gene trees corresponding to the species tree

for t in trees:
    height = []
    row_count = 0
    for speciesnode in speciestree.traverse():
        if speciesnode.is_leaf() == False and speciesnode.is_root() == False and speciesnode != first_int_node: 
            child1 = speciesnode.get_children()[0]
            child2 = speciesnode.get_children()[1]
            sister = speciesnode.get_sisters()[0] 
            if disc.iloc[row_count, col_count] == 'C':
                r_leaves = relevant_leaves(child1, child2, t)
            elif disc.iloc[row_count, col_count] == 'D2':
                r_leaves = relevant_leaves(child1, sister, t)
            elif disc.iloc[row_count, col_count] == 'D1':
                r_leaves = relevant_leaves(child2, sister, t)
            else:
                r_leaves = None
            max_support = 0  #support threshold
            h = -1 #initialize h variable first
            if r_leaves is None:
                height.append('NA')
            else:
                for node in t.traverse():
                    if node.is_root() == False:
                        s = support(node = node, r_leaves = list(r_leaves)) 
                        if s > max_support:
                            max_support = s 
                            h = get_height(node = node)
                if max_support < 1:
                    height.append('NA')
                else:
                    height.append(h)
            row_count += 1
    df['gene' + str(col_count)] = height #height list become a column in the dataframe                               
    col_count += 1 
                                              
#export dataframe
df.to_csv(args.output, index = False, header = True, sep = '\t')

                 

