#! /usr/bin/env python

import treeswift as tsw
import sys

# $1 the reference jplace tree (edge indexed extended newick file)
# $2 the jplace to be reordered
# output: $2 leaves reordered like $1's

# store bracket open/close for convenience in label parsing
BRACKET = {
    '[': ']', # square bracket
    '{': '}', # curly bracket
    "'": "'", # single-quote
    '"': '"', # double-quote
}

INVALID_NEWICK = "Tree not valid Newick tree"


def read_tree_newick(newick):
    '''Read a tree from a Newick string or file

    Args:
        ``newick`` (``str``): Either a Newick string or the path to a Newick file (plain-text or gzipped)

    Returns:
        ``Tree``: The tree represented by ``newick``. If the Newick file has multiple trees (one per line), a ``list`` of ``Tree`` objects will be returned
    '''
    if not isinstance(newick, str):
        try:
            newick = str(newick)
        except:
            raise TypeError("newick must be a str")

    ts = newick.strip()

    try:
        t = tsw.Tree(); t.is_rooted = ts.startswith('[&R]')
        if ts[0] == '[':
            ts = ']'.join(ts.split(']')[1:]).strip(); ts = ts.replace(', ',',')
        n = t.root; i = 0
        while i < len(ts):
            # end of Newick string
            if ts[i] == ';':
                #if i != len(ts)-1 or n != t.root:
                if i != len(ts)-1:
                    raise RuntimeError(INVALID_NEWICK)

            # go to new child
            elif ts[i] == '(':
                c = tsw.Node(); n.add_child(c); n = c

            # go to parent
            elif ts[i] == ')':
                n = n.parent

            # go to new sibling
            elif ts[i] == ',':
                n = n.parent; c = tsw.Node(); n.add_child(c); n = c

            # edge length
            elif ts[i] == ':':
                i += 1; ls = ''
                while ts[i] != ',' and ts[i] != ')' and ts[i] != ';':
                    if ts[i] == "{":
                        ei=''
                        i += 1
                        while ts[i] != "}":
                            ei += ts[i]
                            i += 1
                        n.edge_index = int(ei)
                        break
                    ls += ts[i]; i += 1
                if ls[0] == '[':
                    n.edge_params = ']'.join(ls.split(']')[:-1]); ls = ls.split(']')[-1]
                n.edge_length = float(ls)

            # node label
            else:
                label = ''; bracket = None
                while bracket is not None or ts[i] in BRACKET or (ts[i] != ':' and ts[i] != ',' and ts[i] != ';' and ts[i] != ')'):
                    if ts[i] in BRACKET and bracket is None:
                        bracket = ts[i]
                    elif bracket is not None and ts[i] == BRACKET[bracket]:
                        bracket = None
                    label += ts[i]; i += 1
                i -= 1; n.label = label
            i += 1
    except Exception as e:
        print(e)
        raise RuntimeError("Failed to parse string as Newick: %s"%ts)
    return t

def extended_newick(tree):
    """Newick printing algorithm is based on treeswift"""

    # if tree.root.edge_length is None:
    #     suffix = ''
    # elif isinstance(tree.root.edge_length, int):
    #     suffix = ':%d' % tree.root.edge_length
    # elif isinstance(tree.root.edge_length, float) and tree.root.edge_length.is_integer():
    #     suffix = ':%d' % int(tree.root.edge_length)
    # else:
    #     suffix = ':%s' % str(tree.root.edge_length)
    suffix = ''
    strng = _nodeprint(tree.root)
    if tree.is_rooted:
        return '[&R] %s%s;' % (strng, suffix)
    else:
        return '%s%s;' % (strng, suffix)


def _nodeprint(root):
    node_to_str = dict()

    for node in root.traverse_postorder():
        if node.is_leaf():
            if node.label is None:
                node_to_str[node] = ''
            else:
                node_to_str[node] = str(node.label)
        else:
            out = ['(']
            for c in node.children:
                out.append(node_to_str[c])
                if c.edge_length is not None:
                    if isinstance(c.edge_length, int):
                        l_str = str(c.edge_length)
                    elif isinstance(c.edge_length, float) and c.edge_length.is_integer():
                        l_str = str(int(c.edge_length))
                    else:
                        l_str = str(c.edge_length)
                    out.append(':%s' % l_str)
                out.append('{%d}' % c.edge_index)
                out.append(',')
                del node_to_str[c]
            out.pop()  # trailing comma
            out.append(')')
            if node.label is not None:
                out.append(str(node.label))
            node_to_str[node] = ''.join(out)
    return node_to_str[root]


t1 = read_tree_newick(open(sys.argv[1]).readlines()[0])
t2 = read_tree_newick(open(sys.argv[2]).readlines()[0])

t1l = list([i.label for i in t1.traverse_postorder(internal=False)])
order_guide = dict(zip(t1l, range(1,len(t1l)+1)))

for n in t2.traverse_postorder():
    if n.is_leaf():
        if n.label in order_guide:
            n.av = order_guide[n.label]
            n.num=1
        else:
            n.av = 0
            n.num = 0
    else:
        n.num = sum([x.num for x in n.children])
        if n.num == 0:
            n.av = 0
        else:
            n.av = sum([x.num*x.av for x in n.children])/n.num

for intr in t2.traverse_postorder(internal=True, leaves=False):
    intr.children.sort(key=lambda x: x.av)

print(extended_newick(t2))

