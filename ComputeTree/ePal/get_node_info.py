import networkx as nx
import os

files = ["./tree/" + f for f in os.listdir('./tree/') ]
for file in files:
    # print file
    G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(file))
    print file,
    print len([x for x in G.nodes_iter() ]),
    print len([x for x in G.nodes_iter() if G.out_degree(x)==0 and G.in_degree(x)==1])
    # import pdb
    # pdb.set_trace()



