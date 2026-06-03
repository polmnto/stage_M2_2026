from ete3 import Tree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--treefile")
parser.add_argument("-o", "--output")
args = parser.parse_args()

t = Tree(args.treefile)

#store all taxa names in a list
taxa = []
for leaf in t.get_leaves():
    taxa.append(leaf.name)

#add all those taxa to a root to get a star phylogeny
star = Tree()

for i in taxa:
    star.add_child(name = i)

#export star tree
star.write(outfile = args.output, format = 9)
