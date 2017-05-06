content = open('./llvm_input.dot').readlines()

# find how many nodes
nodes = {}
for c in content:
    if '->' in c:
        print c
        # get rid of semicolon
        temp = c.replace(';', '').strip()
        # get rid of [blah]
        temp = temp.split('[')[0].strip()
        temp_nodes = temp.split(' -> ')
        parent = temp_nodes[0]
        child = temp_nodes[1]
        if parent not in nodes.keys():
            nodes[parent] = []
        nodes[parent].append(child)


import pdb
pdb.set_trace()