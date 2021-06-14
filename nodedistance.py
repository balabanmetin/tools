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


for i in tree1.traverse_postorder(internal=False):
    if i.label != species and i.edge_length > 0:
        rootat1 = i
        break

for j in tree2.traverse_postorder(internal=False):
    if j.label == rootat1.label:
        rootat2 = j
        break

assert rootat1.edge_length-rootat2.edge_length < delta
tree1.reroot(rootat1, rootat1.edge_length/2)
tree2.reroot(rootat2, rootat2.edge_length/2)

tree1.suppress_unifurcations()
tree2.suppress_unifurcations()

# tree1.order(mode="label")
# tree2.order(mode="label")


for i in tree1.traverse_postorder(internal=False):
    if i.label == species:
        q_t1 = i
        break

for j in tree2.traverse_postorder(internal=False):
    if j.label == species:
        q_t2 = j
        break

mrca_list = set()
for n in [q_t1,q_t2]:
    sib = [k for k in n.parent.children if k != n][0]
    mrca_list.add(next(sib.traverse_postorder(internal=False)).label)
    psib = [k for k in n.parent.parent.children if k != n.parent][0]
    mrca_list.add(next(psib.traverse_postorder(internal=False)).label)

mrca1 = tree1.mrca(mrca_list)
mrca2 = tree2.mrca(mrca_list)

dist_to_mrca1 = 0
for p in q_t1.traverse_ancestors(include_self=False):
    if p == tree1.root:
        break
    dist_to_mrca1 += p.edge_length

dist_from_mrca1_to_root=0
for p in mrca1.traverse_ancestors(include_self=True):
    if p == tree1.root:
        break
    dist_from_mrca1_to_root += p.edge_length

dist_to_mrca2 = 0
for p in q_t2.traverse_ancestors(include_self=False):
    if p == tree2.root:
        break
    dist_to_mrca2 += p.edge_length

dist_from_mrca2_to_root=0
for p in mrca2.traverse_ancestors(include_self=True):
    if p == tree2.root:
        break
    dist_from_mrca2_to_root += p.edge_length
print(dist_to_mrca2 + dist_to_mrca1 - 2*dist_from_mrca1_to_root)


