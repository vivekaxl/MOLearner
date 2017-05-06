import matplotlib.pyplot as plt
import numpy as np
problems = ['50-4-5-0-110', '50-4-5-0-90', '50-4-5-4-90', '50-4-5-4-110', 'POM3A', 'POM3B', 'POM3C', 'POM3D', 'xomo_ground', 'xomo_osp', 'xomoo2', 'xomo_all', 'xomo_flight']
N = len(problems)



space = 9
ind = np.arange(space, space * (len(problems) + 1), space)  # the x locations for the groups
width = 1.5  # the width of the bars

fig, ax = plt.subplots()
al2 = [55.0, 53.0, 57.0, 56.0, 47.0, 52.0, 60.0, 47.0, 44.0, 43.0, 43.0, 44.0, 42.0]
rects1 = ax.bar(ind, al2, width, color='#DD451F',label='Flash', log=True)

nsga2 = [2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0]
rects2 = ax.bar(ind + 1 * width, nsga2, width, color='#4B514C',label='NSGAII', log=True)

spea2 = [2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0]
rects3 = ax.bar(ind + 2 * width, spea2, width, color='#447799',label='SPEA2', log=True)

sway = [70.0, 71.0, 75.0, 72.0, 70.0, 71.0, 70.0, 70.0, 68.0, 70.0, 78.0, 70.0, 72.0]
rects3 = ax.bar(ind + 3 * width, sway, width, color='#C3C8CA',label='SWAY', log=True)

ax.set_ylabel('# Evaluations')
# ax.set_title('Scores by group and gender')

ax.set_xticks(ind + 1.5 * width)
ax.set_xticklabels([x for _, x in enumerate(problems)], rotation='90')

ax.set_xlim(5, 127)
ax.set_ylim(0, 3000)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True, frameon=False)

fig.set_size_inches(14, 3.5)
# plt.show()
plt.savefig('config_opti.png', bbox_inches='tight')