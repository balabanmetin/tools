#!/usr/bin/env python

import treeswift as ts
import sys

tree1 = ts.read_tree_newick(sys.argv[1])
tree2 = ts.read_tree_newick(sys.argv[2])
species = sys.argv[3]
delta = 10**-5
# third parameter can be removed. order tree by labels.
# then traverse post order. first time two nodes are different
# one of the two must be "query" . remove query and order again.
# (this don't work if the query is on the same edge in both trees)


# find a leaf with positive branch length.
# locate it in both trees
for i in tree1.traverse_postorder(internal=False):
    if i.label != species and i.edge_length > 0:
        rootat1 = i
        break

for j in tree2.traverse_postorder(internal=False):
    if j.label == rootat1.label:
        rootat2 = j
        break

assert rootat1.edge_length-rootat2.edge_length < delta

# root both trees at the midpoint of the terminal
# edge
tree1.reroot(rootat1, rootat1.edge_length/2)
tree2.reroot(rootat2, rootat2.edge_length/2)

# always suppress unifurcations when rooting with treeswift
tree1.suppress_unifurcations()
tree2.suppress_unifurcations()

# find query species in both trees
for i in tree1.traverse_postorder(internal=False):
    if i.label == species:
        q_t1 = i
        break

for j in tree2.traverse_postorder(internal=False):
    if j.label == species:
        q_t2 = j
        break

# locate the sibling of query in tree1. it's described by
# two leaves under it, one from each side. if the sibling is leaf
# then simply find the label in the second tree. mrca() function
# works for both cases.
sib = [k for k in q_t1.parent.children if k != q_t1][0]
if sib.is_leaf():
    mrca_list = [sib.label]
else:
    mrca_list = [next(i.traverse_postorder(internal=False)).label for i in sib.children]
mrca2 = tree2.mrca(mrca_list)

# the case where the edge is not split by query in tree2
# or the query is placed closer to root:
if mrca2.edge_length > sib.edge_length:
    tree2.reroot(mrca2, sib.edge_length)
    tree2.suppress_unifurcations()
    tot = 0
    for i in q_t2.traverse_ancestors(include_self=False):
        if i.is_root():
            break
        else:
            tot += i.edge_length
    print(tot)
# edge is broken at the exact same spot
# (this should rarely happen in leave one out)
elif mrca2.edge_length == sib.edge_length:
    print(0)
# query is placed on the same edge in tree2 but farther away from
# the root. in this case, we reroot at the parent of mrca2. we don't
# really need to reroot though. we can simply compute the difference
else:
    delta = sib.edge_length - mrca2.edge_length
    print(delta)