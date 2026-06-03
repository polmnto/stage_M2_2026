from ete3 import Tree

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--treefile")
parser.add_argument("-o", "--output")
args = parser.parse_args()

t = Tree(args.treefile)

for node in t.traverse():
    node.name = node.name.replace("_", "")
    node.name = node.name[-9:]
    
t.unroot() #unroot the tree for erable

t.write(outfile = args.output, format = 9) #format 9 = only topology and node names
