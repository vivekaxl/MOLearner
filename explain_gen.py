from __future__ import division
import numpy as np
import os
import sys
from random import shuffle
from utility import lessismore, generational_distance, ranges, inverted_generational_distance
from non_dominated_sort import non_dominated_sort
import math

class rule_entry(object):
    def __init__(self, node_id, attrib_no, threshold, sign):
        """
        :param node_id: Node id of the decision tree
        :param attrib_no: Attribute number or the column number (Starts from 0) 
        :param threshold: Threshold used by the node
        :param sign: <=  or >
        """
        self.node_id = node_id
        self.attrib_no = attrib_no
        self.threshold = threshold
        self.sign = sign

    def __str__(self):
        return " | x[" + str(self.attrib_no) + "] | " + self.sign + " | " + str(self.threshold)



def normalize(x, min, max):
    tmp = float((x - min)) / (max - min + 0.000001)
    if tmp > 1: return 1
    elif tmp < 0: return 0
    else: return tmp

def loss(x1, x2, mins=None, maxs=None):
    # normalize if mins and maxs are given
    if mins and maxs:
        x1 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x1)]
        x2 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x2)]

    o = min(len(x1), len(x2))  # len of x1 and x2 should be equal
    # print x1, x2
    return sum([-1*math.exp((x2i - x1i) / o) for x1i, x2i in zip(x1, x2)]) / o


def get_cdom_values(objectives, lessismore):
    dependents = []
    for rd in objectives:
        temp = []
        for i in xrange(len(lessismore)):
            # if lessismore[i] is true - Minimization else Maximization
            if lessismore[i] is False:
                temp.append(1/rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    maxs = []
    mins = []
    for i in xrange(len(objectives[0])):
         maxs.append(max([o[i] for o in dependents]))
         mins.append(min([o[i] for o in dependents]))

    cdom_scores = []
    for i, oi in enumerate(dependents):
        sum_store = 0
        for j, oj in enumerate(dependents):
            if i!=j:
                # print oi, oj, loss(oi, oj, mins, maxs), loss(oj, oi, mins, maxs)
                if loss(oi, oj, mins, maxs) < loss(oj, oi, mins, maxs):
                    sum_store += 1
        cdom_scores.append(sum_store)
    return cdom_scores


def get_nd_solutions(filename, train_indep, training_dep, testing_indep):
    no_of_objectives = len(training_dep[0])
    predicted_objectives = []
    for objective_no in xrange(no_of_objectives):
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        model.fit(train_indep, [t[objective_no] for t in training_dep])
        predicted = model.predict(testing_indep)
        predicted_objectives.append(predicted)

    # Merge the objectives
    merged_predicted_objectves = []
    for i, j in zip(predicted_objectives[0], predicted_objectives[1]):
        merged_predicted_objectves.append([i, j])
    assert(len(merged_predicted_objectves) == len(predicted_objectives[0])), "Something is wrong"

    # Find Non-Dominated Solutions
    pf_indexes = non_dominated_sort(merged_predicted_objectves, lessismore[filename])
    # print "Number of ND Solutions: ", len(pf_indexes)

    return [testing_indep[i] for i in pf_indexes], [merged_predicted_objectves[i] for i in pf_indexes]


def same_list(list1, list2):
    assert(len(list1) == len(list2)), "Something is wrong"
    for i, j in zip(list1, list2):
        if i!=j: return False
    return True


def get_training_sequence(file, training_indep, training_dep, testing_indep, index=0):
    # build a model and get the predicted non dominated solutions
    return_nd_independent, predicted_objectives = get_nd_solutions(file, training_indep, training_dep, testing_data)
    # For ordering purposes: Add summation of continious domination
    cdom_scores = get_cdom_values(predicted_objectives, lessismore[file])
    assert(len(cdom_scores) == len(predicted_objectives)), "Something is wrong"
    training_sequence = [i[0] for i in sorted(enumerate(cdom_scores), key=lambda x:x[1], reverse=True)]
    assert(len(training_sequence) == len(cdom_scores)), "Something is wrong"
    return training_sequence, return_nd_independent


def not_in_cache(list, listoflist):
    for l in listoflist:
        if same_list(list, l) is True:
            return False
    return True


def get_rules(estimator, indep, dep, lessismore):
    """Given a model of Decision Tree Regressor along with independent values and dependent values, 
    this function would extract the rules to the leaf which has the highest median dependent values"""
    X_train = np.array(indep).astype('float32')
    # Find the leaf id of each samples
    ids = estimator.tree_.apply(X_train)
    feature = estimator.tree_.feature
    threshold = estimator.tree_.threshold

    # Find the best performing leaf
    leaf_ids = set(ids)
    node_repo = []
    for leaf_id in leaf_ids:
        # find indexes of all the data points belonging to this leaf
        indexes = [i for i, l_id in enumerate(ids) if l_id == leaf_id]
        # Collect dependent values
        node_repo.append([leaf_id, np.median([dep[index] for index in indexes])])

    # Leaf_id of the leaf which has the highest median dependent value
    if lessismore is True:
        selected_leaf_id = min(node_repo, key=lambda x: x[1])[0]
    else:
        selected_leaf_id = max(node_repo, key=lambda x: x[1])[0]
    selected_samples = [indep[i] for i, l_id in enumerate(ids) if l_id == selected_leaf_id]

    # From http://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree
    node_indicator = estimator.decision_path(indep)
    # Get all the samples which belongs to the selected leaf
    sample_ids = [i for i, l_id in enumerate(ids) if l_id == selected_leaf_id]

    assert(len(selected_samples) == len(sample_ids)), "Something is wrong"
    rule_list = []

    for i, sample_id in enumerate(sample_ids):
        # Not sure what this does
        node_index = node_indicator.indices[node_indicator.indptr[sample_id]:node_indicator.indptr[sample_id + 1]]
        for node_id in node_index:
            if ids[sample_id] != node_id:
                if X_train[sample_id, feature[node_id]] <= threshold[node_id]:
                    threshold_sign = "<="
                else:
                    threshold_sign = ">"
                if i == 0:
                    rule_list.append(rule_entry(node_id, feature[node_id], threshold[node_id], threshold_sign))
    return rule_list, selected_samples

def explain_me(ex_train_indep, ex_train_dep, lessismore):
    """lessismore is a list"""
    from sklearn.tree import DecisionTreeRegressor, export_graphviz
    # Build two trees
    model1 = DecisionTreeRegressor(min_samples_leaf=len(current_pf))
    model2 = DecisionTreeRegressor(min_samples_leaf=len(current_pf))

    dep1 = [o[0] for o in ex_train_dep]
    dep2 = [o[1] for o in ex_train_dep]

    model1.fit(ex_train_indep, dep1)
    model2.fit(ex_train_indep, dep2)

    export_graphviz(model1, out_file='o1.dot')
    export_graphviz(model2, out_file='o2.dot')

    # os.system("dot -Tpng o1.dot -o o1.png")
    # os.system("dot -Tpng o2.dot -o o2.png")

    # Find rules for obj1
    rules1, _ = get_rules(model1, ex_train_indep, dep1, lessismore[0])

    # Find rules for obj2
    rules2, _ = get_rules(model1, ex_train_indep, dep2, lessismore[1])
    print
    for r in rules1: print r
    print " -- " * 10
    for r in rules2: print r
    import pdb
    pdb.set_trace()


def get_satisfying_entries(data_indep, data_dep, rules):
    condition = ""
    for i, rule in enumerate(rules):
        if i != 0: condition += " and "
        condition += "item[" + str(rule.attrib_no) + "] " + rule.sign + str(rule.threshold)

    return_dep = []
    for i,item in enumerate(data_indep):
        if eval(condition) is True:
            return_dep.append(data_dep[i])

    # if none of the data point satisfies then return random point
    return return_dep


def explain_me_cdom(ex_train_indep, ex_train_dep, lessismore_status, all_data_indep, all_data_dep, current_pf, actual_pf, filename, gen):
    """lessismore is a list"""
    store_data = {}
    assert(len(ex_train_indep) == len(ex_train_dep)), "Something is wrong"
    transformed_training_dep = get_cdom_values(ex_train_dep, lessismore_status)

    from sklearn.tree import DecisionTreeRegressor, export_graphviz
    # Build two trees
    model = DecisionTreeRegressor(min_samples_leaf=len(current_pf))

    model.fit(ex_train_indep, transformed_training_dep)

    export_graphviz(model, out_file='o1.dot')

    # os.system("dot -Tpng o1.dot -o o1.png")
    # os.system("dot -Tpng o2.dot -o o2.png")

    # Find rules for obj
    rules, ss = get_rules(model, ex_train_indep, transformed_training_dep, lessismore_status[0])

    # Find complaint data
    compliant_data_dep = get_satisfying_entries(all_data_indep, all_data_dep, rules)

    try:
        # find convex hull: From http://stackoverflow.com/questions/18169587/get-the-index-of-point-which-create-convexhull
        from scipy.spatial import ConvexHull
        ch = ConvexHull(compliant_data_dep)
        hull_indices = np.unique(ch.simplices.flat)
        convex_hull_points = [compliant_data_dep[i] for i in hull_indices]
    except:
        return -1


    print
    for r in rules: print r

    store_data['all_data_dep'] = all_data_dep
    store_data['convex_hull_x'] = [np.log(compliant_data_dep[i][0]) for i in ch.vertices]
    store_data['convex_hull_y'] = [np.log(compliant_data_dep[i][1]) for i in ch.vertices]
    store_data['complaint_data'] = compliant_data_dep
    store_data['actual_pf'] = actual_pf
    store_data['current_pf'] = current_pf

    import pickle
    pickle.dump(store_data, open('ExplainFiguresPickleLocker/' + filename.split('/')[-1][:-4] + "_" + str(gen) + ".p", 'w'))

    import matplotlib.pyplot as plt
    plt.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.')
    plt.fill([np.log(compliant_data_dep[i][0]) for i in ch.vertices], [np.log(compliant_data_dep[i][1]) for i in ch.vertices], 'k', alpha=0.3)
    plt.scatter([np.log(p[0]) for p in compliant_data_dep], [np.log(p[1]) for p in compliant_data_dep], color='yellow', marker='+',
                   label="Explain-PF")
    l2, = plt.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
                   label="Predicted-PF")
    l3, = plt.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
    plt.xlabel('log(f1)')
    plt.ylabel('log(f2)')
    plt.legend(loc=2)
    plt.savefig('./ExplainFiguresGen/' + filename.split('/')[-1][:-4] + "_" + str(gen) + ".png")
    plt.cla()


def explain_me_nds(ex_train_indep, ex_train_dep, lessismore_status, all_data_indep, all_data_dep, current_pf, actual_pf, nds_points, filename, gen):
    """lessismore is a list"""
    store_data = {}
    assert(len(ex_train_indep) == len(ex_train_dep)), "Something is wrong"
    transformed_training_dep = get_cdom_values(ex_train_dep, lessismore_status)

    from sklearn.tree import DecisionTreeRegressor, export_graphviz
    # Build two trees
    model = DecisionTreeRegressor(min_samples_leaf=len(current_pf))

    model.fit(ex_train_indep, transformed_training_dep)

    export_graphviz(model, out_file='o1.dot')

    # os.system("dot -Tpng o1.dot -o o1.png")
    # os.system("dot -Tpng o2.dot -o o2.png")


    try:
        # find convex hull: From http://stackoverflow.com/questions/18169587/get-the-index-of-point-which-create-convexhull
        from scipy.spatial import ConvexHull
        ch = ConvexHull(nds_points)
        hull_indices = np.unique(ch.simplices.flat)
        convex_hull_points = [nds_points[i] for i in hull_indices]
    except:
        return -1


    store_data['all_data_dep'] = all_data_dep
    store_data['convex_hull_x'] = [np.log(nds_points[i][0]) for i in ch.vertices]
    store_data['convex_hull_y'] = [np.log(nds_points[i][1]) for i in ch.vertices]
    store_data['complaint_data'] = nds_points
    store_data['actual_pf'] = actual_pf
    store_data['current_pf'] = current_pf

    import pickle
    pickle.dump(store_data, open('ExplainFiguresPickleLocker/' + filename.split('/')[-1][:-4] + "_" + str(gen) + ".p", 'w'))

    import matplotlib.pyplot as plt
    plt.scatter([np.log(d[0]) for d in all_data_dep], [np.log(d[1]) for d in all_data_dep], color='r', marker='.')
    plt.fill([np.log(nds_points[i][0]) for i in ch.vertices], [np.log(nds_points[i][1]) for i in ch.vertices], 'k', alpha=0.3)
    plt.scatter([np.log(p[0]) for p in nds_points], [np.log(p[1]) for p in nds_points], color='yellow', marker='+',
                   label="Explain-PF")
    l2, = plt.plot([np.log(p[0]) for p in current_pf], [np.log(p[1]) for p in current_pf], color='green', marker='o',
                   label="Predicted-PF")
    l3, = plt.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='blue', marker='v', label="Actual-PF")
    plt.xlabel('log(f1)')
    plt.ylabel('log(f2)')
    plt.legend(loc=2)
    plt.savefig('./ExplainFiguresGen/' + filename.split('/')[-1][:-4] + "_" + str(gen) + ".png")
    plt.cla()


if __name__ == "__main__":
    from utility import read_file, split_data, build_model
    files = ['./Data/llvm_input.csv',
             # './Data/noc_CM_log.csv',
             #  './Data/sort_256.csv',
             # './Data/wc+rs-3d-c4.csv', './Data/wc+sol-3d-c4.csv', './Data/wc+wc-3d-c4.csv',
             # './Data/wc-3d-c4.csv', './Data/wc-5d-c5.csv', './Data/wc-6d-c1.csv', './Data/wc-c1-3d-c1.csv',
             # './Data/wc-c3-3d-c1.csv', './Data/rs-6d-c3.csv'
             ]

    all_data = {}
    initial_sample_size = 20
    for file in files:
        all_data[file] = {}
        all_data[file]['evals'] = []
        all_data[file]['gen_dist'] = []
        all_data[file]['igd'] = []

        print file
        data = read_file(file)

        # Creating Objective Dict
        objectives_dict = {}

        for d in data:
            key = ",".join(map(str, d.decisions))
            objectives_dict[key] = d.objectives

        def get_evals():
            return sum(1 if counting_dict[key]>0 else 0 for key in counting_dict.keys())

        evals = []
        pfs = []
        for rep in xrange(1):
            print ". ",
            sys.stdout.flush()
            shuffle(data)

            lives = 10
            training_data = [d.decisions for d in data[:initial_sample_size]]
            testing_data = [d.decisions for d in data]
            evaluation_count = 0
            previous_pf = []

            counting_dict = {}
            for d in data:
                key = ",".join(map(str, d.decisions))
                counting_dict[key] = 0

            gen = 0
            while True:
                # Creating Count Dict -- To make sure that if a point is evaluated twice, it is counted as once


                def get_evals():
                    return sum(1 if counting_dict[key]>0 else 0 for key in counting_dict.keys())

                def get_objective_score(independent):
                    key = ",".join(map(str, independent))
                    # print "@@ ", counting_dict[key]
                    counting_dict[key] += 1
                    # print "@@| ", counting_dict[key]
                    return objectives_dict[key]


                training_dep = [get_objective_score(r) for r in training_data]

                training_sequence, return_nd_independent = get_training_sequence(file, training_data, training_dep, testing_data)
                assert(len(training_sequence) == len(return_nd_independent)), "Soemthing is wrong"
                next_point = testing_data[training_sequence[0]]
                count = 1
                while not_in_cache(next_point, training_data) is False and count < len(training_sequence):
                    next_point = return_nd_independent[training_sequence[count]]
                    count += 1
                    # print "# ", #next_point
                    sys.stdout.flush()

                # print
                next_point_dependent = get_objective_score(next_point)


                # Add it to training set and see if it is a dominating point
                before_pf_indexes = non_dominated_sort(training_dep, lessismore[file])
                before_pf = [training_dep[i] for i in before_pf_indexes]

                added_training = training_data + [next_point]

                after_pf_indexes = non_dominated_sort(training_dep + [next_point_dependent], lessismore[file])
                after_pf = [(training_dep + [next_point_dependent])[i] for i in after_pf_indexes]

                import itertools
                after_pf.sort()
                after_pf = [k for k, _ in itertools.groupby(after_pf)]

                # See if the new point is a dominant point
                previously_seen = []
                previously_not_seen = []
                for cr in after_pf:
                    seen = False
                    for pr in before_pf:
                        # Previously Seen
                        if same_list(pr, cr):
                            seen = True
                            previously_seen.append(cr)
                            continue
                    if seen is False:
                        previously_not_seen.append(cr)

                if len(previously_not_seen) == 0:
                    lives -= 1

                training_data = training_data + [next_point]

                gen += 1
                training_dependent = [get_objective_score(r) for r in training_data]
                pf_indexes = non_dominated_sort(training_dependent, lessismore[file])
                t_current_pf = sorted([training_dependent[i] for i in pf_indexes], key=lambda x: x[0])
                actual_dependent = [get_objective_score(d) for d in testing_data]
                true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file])
                true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x: x[0])
                explain_me_cdom([training_data[i] for i in pf_indexes], [training_dependent[i] for i in pf_indexes],
                                lessismore[file], testing_data, [get_objective_score(d) for d in testing_data],
                                t_current_pf, true_pf, file, gen)

                if lives == 0: break

            print "Size of the frontier = ", len(training_data), " Evals: ", get_evals(),
            # Calculate the True ND
            training_dependent = [get_objective_score(r) for r in training_data]
            pf_indexes = non_dominated_sort(training_dependent, lessismore[file])
            current_pf = [training_dependent[i] for i in pf_indexes]
            all_data[file]['evals'].append(get_evals())

            actual_dependent = [get_objective_score(d) for d in testing_data]
            true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file])
            true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])
            current_pf = sorted(current_pf, key=lambda x:x[0])
            from utility import draw_pareto_front
            # draw_pareto_front(actual_dependent, true_pf, current_pf)
            all_data[file]['gen_dist'].append(generational_distance(true_pf, current_pf, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(true_pf, current_pf, ranges[file]))

            # explain_me_cdom(training_data, [get_objective_score(indep) for indep in training_data], lessismore[file], testing_data, [get_objective_score(d) for d in testing_data], current_pf, true_pf, file)


            print " GD: ",  all_data[file]['gen_dist'][-1],
            print " IGD: ",  all_data[file]['igd'][-1]



        print [round(x, 5) for x in all_data[file]['evals']]
        print [round(x, 5) for x in all_data[file]['gen_dist']]
        print [round(x, 5) for x in all_data[file]['igd']]


    import pickle
    pickle.dump(all_data, open('al-based-2.p', 'w'))
