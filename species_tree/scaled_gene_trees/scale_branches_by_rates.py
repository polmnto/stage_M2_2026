from ete3 import Tree
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--treefile")
parser.add_argument("-r", "--rate") 
parser.add_argument("-o", "--output") 
args = parser.parse_args()

#list of gene trees
trees = []
for line in open(args.treefile):
    t = Tree(line)
    trees.append(t)
    
#list of rates computed by erable
data_rate = pd.read_table(args.rate, sep = " ")   
rate_column = data_rate["rate"] 

rates = []
for row in rate_column:
    rates.append(row)
    
#divide each gene tree branch lengths by erable rates
x = 0
for t in trees:
    for node in t.traverse():
        node.dist = node.dist / rates[x]
    x += 1

#export scaled gene trees 
f = open(args.output, "a+")

for t in trees:
    f.write(t.write())
    f.write("\n")
    
f.close()


