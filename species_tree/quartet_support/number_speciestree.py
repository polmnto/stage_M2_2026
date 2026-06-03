from ete3 import Tree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speciestree")
parser.add_argument("-o", "--output")
args = parser.parse_args()


species = Tree(args.speciestree)

name_nb = 1
for node in species.traverse(): 
    if node.is_leaf() == False and node.is_root() == False:
        node.name = name_nb
        name_nb +=1

species.write(outfile = args.output, format = 1)
