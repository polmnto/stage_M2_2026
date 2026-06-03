from ete3 import Tree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--treefile")
parser.add_argument("-o", "--output")
args = parser.parse_args()

#list of gene trees
trees = []

for line in open(args.treefile):
    t = Tree(line)
    trees.append(t)
    
#unroot the gene trees
for t in trees:
    t.unroot()

#create a distance matrix file in phylip format
f = open(args.output, "a+")

f.write(str(len(trees)))
f.write("\n")

for t in trees:
    f.write("\n")
    f.write(str(len(t.get_leaves()))) #print the species number
    f.write(" ")
    f.write("1") #usually the sequence length, here = 1 by default
    f.write("\n")
    for i in t.get_leaves():
        i.name = i.name.replace("_", "")   #remove the underscores
        if len(i.name) > 9: #limit species names to 9 characters
            f.write(i.name[-9:])  
            f.write(" ")
        else:
            f.write(i.name) #fill the space if name length < 9
            f.write(str(" ")*(9-len(i.name)))
            f.write(" ")
        for j in t.get_leaves(): #get distance between each i and j taxon
            d = t.get_distance(t&i.name,t&j.name)      
            if d == 0:    #limite character number to 10 for each distance value
                f.write("0.00000000")
                f.write(" ")
            elif len(str(d)) <= 10 or 'e' in str(d):
                f.write(str(format(d, 'f')))  #f for "fixed point number format" > write numbers as 0.000023 instead of 2.3e-6 for example
                f.write(str(0)*(10-len(str(format(d, 'f')))))
                f.write(" ")
            else:
                f.write(str(d)[:10])
                f.write(" ")
        f.write("\n")
f.close()

        

