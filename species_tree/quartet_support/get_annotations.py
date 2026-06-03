from ete3 import Tree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--treefile")
parser.add_argument("-o", "--outputcsv")
args = parser.parse_args()

#import scored species tree
t = Tree(args.treefile, format = 1, quoted_node_names = True)

f = open(args.outputcsv, "w+")
f.write("node_ID;q1;q2;q3;f1;f2;f3;pp1;pp2;pp3;QC;EN") #column names
f.write("\n")

#export a table with node annotations
n = 1
for node in t.traverse():
    if node.is_leaf() == False and node.is_root() == False:
        node.name = "[" + str(n) + ";" + node.name[1:] #number each node
        if n !=1:   #prevent getting an empty first line (as the 1st node cannot be scored with quartet support because it doesn't have 4 clusters around it)
            name = node.name.replace("q1=", "").replace("q2=", "").replace("q3=", "").replace("f1=", "").replace("f2=", "").replace("f3=", "").replace("pp1=", "").replace("pp2=", "").replace("pp3=", "").replace("QC=", "").replace("EN=", "")   #only keeps numbered values
            f.write(name[1:-1]) #delete brackets
            f.write("\n")
        n += 1
f.close()
