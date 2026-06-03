from ete3 import Tree
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--treefile") #scored gene trees
parser.add_argument("-o", "--output")
args = parser.parse_args()

#import scored trees
trees = []
for line in open(args.treefile):
    t = Tree(line, format = 1, quoted_node_names = True)
    trees.append(t)
    
#create the first column of the datafram with node numbers
ref_tree = trees[0]
nodes = []
n = 1

for node in ref_tree.traverse():
    if node.is_leaf() == False and node.is_root() == False:
        nodes.append(n)
        n += 1

data = {'node': nodes}
df = pd.DataFrame(data)

#get scores for each gene tree and store it in a new column
gene = 1

for t in trees:
    quartet_support = []
    for node in t.traverse():
        if node.is_leaf() == False and node.is_root() == False:
            name = node.name.replace("q1=", "").replace("q2=", "").replace("q3=", "").replace("[", "").replace("]", "").replace(";", "|")
            quartet_support.append(name)
    df['gene' + str(gene)] = quartet_support
    gene += 1
    
df = df.drop([0]) #remove the empty first row
    
#export dataframe    
df.to_csv(args.output, index = False, header = True, sep = '\t') 
