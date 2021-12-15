import treeswift as ts
import sys

# $1 tree
# $2 target subtree leaves
t=ts.read_tree_newick(sys.argv[1])
leaves_t = set([i.label for i in t.traverse_postorder(internal=False)])
with open(sys.argv[2]) as f:
    leaves_sub  = set(list(map( lambda x: x.strip(), f.readlines())))
intr = list(leaves_t.intersection(leaves_sub))
print(t.extract_tree_with(intr))


