from Bio import Phylo
from cStringIO import StringIO
    
# outputs number of clusters, and the longest path to any leaf connected to the
# root.
def cluster(tree, threshold):
    return recurse_cluster(tree.clade, threshold)

def recurse_cluster(clade, threshold):
        children = clade.clades
        if len(children) == 0:
            return (1,0)
        elif len(children) != 2:
		raise ValueError('Tree is not full binary')
        else:
		nl,dl = recurse_cluster(children[0], threshold)
		nr,dr = recurse_cluster(children[1], threshold)
                wl = children[0].branch_length
                wr = children[1].branch_length
                if dl+dr+wl+wr > threshold:
                    return (nl+nr, min(dl+wl, dr+wr))
                else:
                    return (nl+nr-1, max(dl+wl, dr+wr))
trees= [
"(A:9,B:9)",
"(A:1,B:1)",
"((A:1,B:1):9,C:1)",
"((A:1,B:1):9,(C:1,D:1):9)",
"((A:9,B:1):1,(C:1,D:9):1)",
"(((A:5,B:3):1,C:1):9,D:9)",
"(((A:5,B:5):1,C:1):9,D:9)"
]

for treedata in trees:
    handle = StringIO(treedata)
    tree = Phylo.read(handle, "newick")
    Phylo.draw_ascii(tree)
    print(cluster(tree, 7))
