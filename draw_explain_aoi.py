import pickle
import numpy as np
import matplotlib.pyplot as plt


f, ((ax1, ax2), (ax5, ax7)) = plt.subplots(2, 2)


c = pickle.load(open("./ExplainFiguresPickleLocker2/llvm_input_1.p"))
all_data_dep = c['all_data_dep']
convex_hull_x = c['convex_hull_x']
convex_hull_y = c['convex_hull_y']
compliant_data_dep = c['complaint_data']
current_pf = c['current_pf']
actual_pf = c['actual_pf']

l1 = ax1.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.', s=2)
l2 = ax1.fill(convex_hull_x, convex_hull_y, 'k', alpha=0.3)
l3 = ax1.scatter([np.log(p[0]) for p in compliant_data_dep], [np.log(p[1]) for p in compliant_data_dep], color='#D7EA00', marker='+',
               label="Explain-PF")
l4 = ax1.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
               label="Predicted-PF")
l5 = ax1.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
ax1.set_title('Iteration 1 - (' + str(len(compliant_data_dep)) + ')', fontsize=10)
ax1.set_xlabel('log(f1)', fontsize=10)
ax1.set_ylabel('log(f2)', fontsize=10)
# ax1.tick_params(axis='x', which='minor', bottom='off', top='off', labelbottom='off')

c = pickle.load(open("./ExplainFiguresPickleLocker2/llvm_input_4.p"))
all_data_dep = c['all_data_dep']
convex_hull_x = c['convex_hull_x']
convex_hull_y = c['convex_hull_y']
compliant_data_dep = c['complaint_data']
current_pf = c['current_pf']
actual_pf = c['actual_pf']

ax2.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.', s=2)
ax2.fill(convex_hull_x, convex_hull_y, 'k', alpha=0.3)
ax2.scatter([np.log(p[0]) for p in compliant_data_dep], [np.log(p[1]) for p in compliant_data_dep], color='#D7EA00', marker='+',
               label="Explain-PF")
ax2.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
               label="Predicted-PF")
ax2.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
# ax2.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
ax2.set_title('Iteration 4 - (' + str(len(compliant_data_dep)) + ')', fontsize=10)
ax2.set_xlabel('log(f1)', fontsize=10)
ax2.set_ylabel('log(f2)', fontsize=10)

c = pickle.load(open("./ExplainFiguresPickleLocker2/llvm_input_8.p"))
all_data_dep = c['all_data_dep']
convex_hull_x = c['convex_hull_x']
convex_hull_y = c['convex_hull_y']
compliant_data_dep = c['complaint_data']
current_pf = c['current_pf']
actual_pf = c['actual_pf']

# ax3.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.')
# ax3.fill(convex_hull_x, convex_hull_y, 'k', alpha=0.3)
# ax3.scatter([np.log(p[0]) for p in compliant_data_dep], [np.log(p[1]) for p in compliant_data_dep], color='#D7EA00', marker='+',
#                label="Explain-PF")
# ax3.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
#                label="Predicted-PF")
# ax3.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
# ax3.set_title('Iteration 8 - (' + str(len(compliant_data_dep)) + ')', fontsize=10)
# ax3.set_xlabel('log(f1)', fontsize=10)
# ax3.set_ylabel('log(f2)', fontsize=10)

c = pickle.load(open("./ExplainFiguresPickleLocker2/llvm_input_12.p"))
all_data_dep = c['all_data_dep']
convex_hull_x = c['convex_hull_x']
convex_hull_y = c['convex_hull_y']
compliant_data_dep = c['complaint_data']
current_pf = c['current_pf']
actual_pf = c['actual_pf']

ax5.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.', s=2)
ax5.fill(convex_hull_x, convex_hull_y, 'k', alpha=0.3)
ax5.scatter([np.log(p[0]) for p in compliant_data_dep], [np.log(p[1]) for p in compliant_data_dep], color='#D7EA00', marker='+',
               label="Explain-PF")
ax5.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
               label="Predicted-PF")
ax5.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
# ax5.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
ax5.set_title('Iteration 12 - (' + str(len(compliant_data_dep)) + ')', fontsize=10)
ax5.set_xlabel('log(f1)', fontsize=10)
ax5.set_ylabel('log(f2)', fontsize=10)

c = pickle.load(open("./ExplainFiguresPickleLocker2/llvm_input_15.p"))
all_data_dep = c['all_data_dep']
convex_hull_x = c['convex_hull_x']
convex_hull_y = c['convex_hull_y']
compliant_data_dep = c['complaint_data']
current_pf = c['current_pf']
actual_pf = c['actual_pf']

# ax6.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.')
# ax6.fill(convex_hull_x, convex_hull_y, 'k', alpha=0.3)
# ax6.scatter([np.log(p[0]) for p in compliant_data_dep], [np.log(p[1]) for p in compliant_data_dep], color='#D7EA00', marker='+',
#                label="Explain-PF")
# ax6.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
#                label="Predicted-PF")
# ax6.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
# ax6.set_title('Iteration 15 - (' + str(len(compliant_data_dep)) + ')', fontsize=10)
# ax6.set_xlabel('log(f1)', fontsize=10)
# ax6.set_ylabel('log(f2)', fontsize=10)
# # ax6.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

c = pickle.load(open("./ExplainFiguresPickleLocker2/llvm_input_16.p"))
all_data_dep = c['all_data_dep']
convex_hull_x = c['convex_hull_x']
convex_hull_y = c['convex_hull_y']
compliant_data_dep = c['complaint_data']
current_pf = c['current_pf']
actual_pf = c['actual_pf']

ax7.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.', label='all-points', s=2)
ax7.fill(convex_hull_x, convex_hull_y, 'k', alpha=0.3)
ax7.scatter([np.log(p[0]) for p in compliant_data_dep], [np.log(p[1]) for p in compliant_data_dep], color='#D7EA00', marker='+',
               label="Explain-PF")
ax7.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
               label="Predicted-PF")
ax7.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
ax7.set_title('Iteration 16 - (' + str(len(compliant_data_dep)) + ')', fontsize=10)
ax7.set_xlabel('log(f1)', fontsize=10)
ax7.set_ylabel('log(f2)', fontsize=10)
# ax7.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

for ax in [ax1, ax2, ax5, ax7]:
    plt.sca(ax)
    plt.xticks(rotation=90)
    ax.tick_params(labelsize=6)


plt.figlegend([ax1.lines[0], ax1.lines[1], l3, l1], [ "Predicted-PF", "Actual-PF", "Points of Interest", "Feasible Solutions"], frameon=False, loc='lower center', bbox_to_anchor=(0.48, -0.015), fancybox=True, ncol=4, fontsize=10)
f.tight_layout()
plt.savefig('temp_explain_aoi.png', bbox_inches='tight')