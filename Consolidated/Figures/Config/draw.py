import matplotlib.pyplot as plt
import numpy as np
problems = ['wc-c1-3d-c1', 'sort_256', 'wc-c3-3d-c1', 'wc+wc-3d-c4', 'wc-3d-c4', 'wc+rs-3d-c4', 'wc+sol-3d-c4', 'noc_CM_log', 'wc-5d-c5', 'rs-6d-c3', 'wc-6d-c1', 'llvm_input', 'TriMesh', 'x264-DB', 'SaC',]
N = len(problems)



space = 9
ind = np.arange(space, space * (len(problems) + 1), space)  # the x locations for the groups
width = 1.5  # the width of the bars

fig, ax = plt.subplots()
al2 = [29.0, 25.0, 29.0, 37.0, 35.0, 37.0, 36.0, 32.0, 29.0, 35.0, 36.0, 33.0, 37.0, 36.0, 31.0]
rects1 = ax.bar(ind, al2, width, color='#DD451F',label='Flash')

epal1 = [112.0, 86.0, 248.0, 120.0, 210.0, 139.0, 132.0, 53.0, 48.0, 187.0, 215.0, 69.0, 0, 0, 0]
rects2 = ax.bar(ind + 1 * width, epal1, width, color='#4B514C',label='ePAL-0.01')

epal3 = [74.0, 20.0, 101.0, 69.0, 55.0, 71.0, 73.0, 29.0, 30.0, 30.0, 140.0, 35.0, 0, 126, 0]
rects3 = ax.bar(ind + 2 * width, epal3, width, color='#447799',label='ePal-0.3')


ax.set_ylabel('# Evaluations')
# ax.set_title('Scores by group and gender')

ax.set_xticks(ind + 1.5 * width)
ax.set_xticklabels(['SS' + str(i+1) for i,_ in enumerate(problems)], rotation='90')

# ax.set_xlim(3, 157)

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True, frameon=False)

fig.set_size_inches(14, 3.5)
# plt.show()
plt.savefig('config_eval.png', bbox_inches='tight')