import pickle
import numpy as np

epal = pickle.load(open('./Data/epal_output.p'))
flash = pickle.load(open('./Data/flash_output.p'))

config_systems = ['wc-c1-3d-c1', 'sort_256', 'wc-c3-3d-c1', 'wc+wc-3d-c4', 'wc-3d-c4', 'wc+rs-3d-c4', 'wc+sol-3d-c4', 'noc_cm', 'wc-5d-c5', 'rs-6d-c3', 'wc-6d-c1', 'llvm']

mapping = {
            'noc_cm': 'noc_CM_log',
            'llvm': 'llvm_input',
            'POM3A': 'pom3a',
            'POM3B': 'pom3b',
            'POM3C': 'pom3c',
            'POM3D': 'pom3d',
           }

# For nodes
epal_001_nodes = [np.median([i[0] for i in epal[system+"_0.01"]]) for system in config_systems]
epal_03_nodes = [np.median([i[0] for i in epal[system+"_0.3"]]) for system in config_systems]
c_flash_nodes = [np.median([i[0] for i in flash[system]]) if system in flash.keys() else np.median([i[0] for i in flash[mapping[system]]]) for system in config_systems]

# For leaf nodes
epal_001_lnodes = [np.median([i[1] for i in epal[system+"_0.01"]]) for system in config_systems]
epal_03_lnodes = [np.median([i[1] for i in epal[system+"_0.3"]]) for system in config_systems]
c_flash_lnodes = [np.median([i[1] for i in flash[system]]) if system in flash.keys() else np.median([i[1] for i in flash[mapping[system]]]) for system in config_systems]

problems = ['MONRP_50_4_5_0_90', 'MONRP_50_4_5_0_110', 'MONRP_50_4_5_4_90', 'MONRP_50_4_5_4_110', 'POM3A', 'POM3B', 'POM3C', 'POM3D', 'xomo_ground', 'xomo_osp', 'xomoo2', 'xomo_all', 'xomo_flight']
names = ['50-4-5-0-90', '50-4-5-0-110', '50-4-5-4-90', '50-4-5-4-110', 'POM3A', 'POM3B', 'POM3C', 'POM3D', 'ground', 'osp', 'xomoo2', 'all', 'flight']

moead = pickle.load(open('./Data/moead_output.p'))
nsga2 = pickle.load(open('./Data/nsgaii_output.p'))
spea2 = pickle.load(open('./Data/spea2_output.p'))
sway = pickle.load(open('./Data/sway_output.p'))


cp_flash_nodes = [np.median([i[0] for i in flash[problem]]) if problem in flash.keys() else np.median([i[0] for i in flash[mapping[problem]]]) for problem in problems]
moead_nodes = [np.median([i[0] for i in moead[problem]]) if problem in moead.keys() else np.median([i[0] for i in moead[mapping[problem]]]) for problem in problems]
nsga2_nodes = [np.median([i[0] for i in nsga2[problem]]) if problem in nsga2.keys() else np.median([i[0] for i in nsga2[mapping[problem]]]) for problem in problems]
spea2_nodes = [np.median([i[0] for i in spea2[problem]]) if problem in spea2.keys() else np.median([i[0] for i in spea2[mapping[problem]]]) for problem in problems]
sway_nodes = [np.median([i[0] for i in sway[problem]]) if problem in sway.keys() else np.median([i[0] for i in sway[mapping[problem]]]) for problem in problems]

cp_flash_lnodes = [np.median([i[1] for i in flash[problem]]) if problem in flash.keys() else np.median([i[1] for i in flash[mapping[problem]]]) for problem in problems]
moead_lnodes = [np.median([i[1] for i in moead[problem]]) if problem in moead.keys() else np.median([i[0] for i in moead[mapping[problem]]]) for problem in problems]
nsga2_lnodes = [np.median([i[1] for i in nsga2[problem]]) if problem in nsga2.keys() else np.median([i[0] for i in nsga2[mapping[problem]]]) for problem in problems]
spea2_lnodes = [np.median([i[1] for i in spea2[problem]]) if problem in spea2.keys() else np.median([i[0] for i in spea2[mapping[problem]]]) for problem in problems]
sway_lnodes = [np.median([i[1] for i in sway[problem]]) if problem in sway.keys() else np.median([i[0] for i in sway[mapping[problem]]]) for problem in problems]


space = 9
space2 = 12

ind1 = np.arange(space, space * (len(config_systems) + 1), space)  # the x locations for the groups
ind2 = np.arange(space2, space2 * (len(problems) + 1), space2)  # the x locations for the groups
width = 1.5  # the width of the bars

print ind1
print ind2

import matplotlib.pyplot as plt
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.bar(ind1, c_flash_nodes, width, color='#DD451F',label='Flash')
a = ax1.bar(ind1 + 1 * width, epal_001_nodes, width, color='#4B514C',label='ePAL-0.01')
b = ax1.bar(ind1 + 2 * width, epal_03_nodes, width, color='#447799',label='ePal-0.3')
ax1.set_xticks(ind1 + 1.5 * width)
ax1.set_xticklabels(['SS' + str(i+1) for i,_ in enumerate(problems)], rotation='30')
ax1.set_ylabel('# of Nodes')
ax1.tick_params(axis='both', which='major', labelsize=10)

ax2.bar(ind1, c_flash_lnodes, width, color='#DD451F',label='Flash')
ax2.bar(ind1 + 1 * width, epal_001_lnodes, width, color='#4B514C',label='ePAL-0.01')
ax2.bar(ind1 + 2 * width, epal_03_lnodes, width, color='#447799',label='ePal-0.3')
ax2.set_xticks(ind1 + 1.5 * width)
ax2.set_xticklabels(['SS' + str(i+1) for i,_ in enumerate(problems)], rotation='30')
ax2.set_ylabel('# of Leaves')
ax2.tick_params(axis='both', which='major', labelsize=10)

c = ax3.bar(ind2, cp_flash_nodes, width, color='#DD451F',label='Flash')
d = ax3.bar(ind2 + 1 * width, nsga2_nodes, width, color='#D8DBE2',label='NSGAII')
e = ax3.bar(ind2 + 2 * width, spea2_nodes, width, color='#B09E99',label='SPEA2')
f = ax3.bar(ind2 + 3 * width, moead_nodes, width, color='#4DA6AC',label='MOEAD')
g = ax3.bar(ind2 + 4 * width, sway_nodes, width, color='#197278',label='SWAY')
ax3.set_xlim(5, 170)
ax3.set_xticks(ind2 - 1.5* width)
ax3.set_xticklabels(names, rotation='30')
ax3.set_ylabel('# of Nodes')
ax3.tick_params(axis='both', which='major', labelsize=10)

ax4.bar(ind2, cp_flash_lnodes, width, color='#DD451F',label='Flash')
ax4.bar(ind2 + 1 * width, nsga2_lnodes, width, color='#D8DBE2',label='NSGAII')
ax4.bar(ind2 + 2 * width, spea2_lnodes, width, color='#B09E99',label='SPEA2')
ax4.bar(ind2 + 3 * width, moead_lnodes, width, color='#4DA6AC',label='MOEAD')
ax4.bar(ind2 + 4 * width, sway_lnodes, width, color='#197278',label='SWAY')
ax4.set_xlim(5, 170)
ax4.set_xticks(ind2 - 1.5* width)
ax4.set_xticklabels(names, rotation='30')
ax4.set_ylabel('# of Leaves')
ax4.tick_params(axis='both', which='major', labelsize=10)

plt.minorticks_off()
plt.figlegend([c, a, b, d, e, f, g,], ['FLASH','ePAL-0.01', 'ePAL-0.3', 'NSGAII', 'SPEA2', 'MOEA/D', 'SWAY'], loc='upper center', bbox_to_anchor=(0.45, 1.05), ncol=7, fancybox=True, frameon=False)
fig.set_size_inches(15, 6)
# plt.show()
plt.savefig('explain.png', bbox_inches='tight')
