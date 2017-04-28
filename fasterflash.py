from __future__ import division
import numpy as np
import os
import sys
from random import shuffle, randint
from utility import lessismore, generational_distance, ranges,inverted_generational_distance
from non_dominated_sort_fast import non_dominated_sort_fast
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
        return str(self.node_id) + " | " + str(self.attrib_no) + " | " + self.sign + " | " + str(self.threshold)


def normalize(x, min, max):
    tmp = float((x - min)) / (max - min + 0.000001)
    if tmp > 1:
        return 1
    elif tmp < 0:
        return 0
    else:
        return tmp


def loss(x1, x2, mins=None, maxs=None):
    # normalize if mins and maxs are given
    if mins and maxs:
        x1 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x1)]
        x2 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x2)]

    o = min(len(x1), len(x2))  # len of x1 and x2 should be equal
    return sum([-1 * math.exp((x2i - x1i) / o) for x1i, x2i in zip(x1, x2)]) / o


def get_cdom_values(objectives, lessismore):
    """This function consume a dataset and replaces the objective values with the 
    number of points it dominates in the dataset"""
    dependents = []
    # transforming objectives to fit minimization or maximization tasks
    for rd in objectives:
        temp = []
        for i in xrange(len(lessismore)):
            # if lessismore[i] is true - Minimization else Maximization
            if lessismore[i] is False:
                temp.append(1 / rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    # Find ranges for normalization
    maxs = []
    mins = []
    for i in xrange(len(objectives[0])):
        maxs.append(max([o[i] for o in dependents]))
        mins.append(min([o[i] for o in dependents]))

    # Doing all pair comparison to build the cdom_scores.
    cdom_scores = []
    for i, oi in enumerate(dependents):
        sum_store = 0
        for j, oj in enumerate(dependents):
            if i != j:
                # print oi, oj, loss(oi, oj, mins, maxs), loss(oj, oi, mins, maxs)
                if loss(oi, oj, mins, maxs) < loss(oj, oi, mins, maxs):
                    sum_store += 1
        cdom_scores.append(sum_store)

    for i in xrange(len(objectives)):
        assert (cdom_scores[i] <= len(objectives)), "Something is wrong"

    return cdom_scores


def get_rules(estimator, indep, transform_dep):
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
        node_repo.append([leaf_id, np.median([transform_dep[index] for index in indexes])])

    # Leaf_id of the leaf which has the highest median dependent value
    selected_leaf_id = max(node_repo, key=lambda x: x[1])[0]
    selected_samples =[indep[i] for i, l_id in enumerate(ids) if l_id == selected_leaf_id]

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


def get_satisfying_entries(training_data, data, rules):
    def same_list(lista, listb):
        for a,b in zip(lista, listb):
            if a != b: return False
        return True

    condition = ""
    for i, rule in enumerate(rules):
        if i != 0: condition += " and "
        condition += "item[" + str(rule.attrib_no) + "] " + rule.sign + str(rule.threshold)
    for item in data:
        if eval(condition) is True:
            cont = False
            for train in training_data:
                if same_list(train, item) is True:
                    cont = True
                    break
            if cont is not True:
                return [item]


    # if none of the data point satisfies then return random point
    return [data[randint(0, len(data)-1)]]


def not_in_cache(list, listoflist):
    for l in listoflist:
        if same_list(list, l) is True:
            return False
    return True


def same_list(list1, list2):
    assert(len(list1) == len(list2)), "Something is wrong"
    for i, j in zip(list1, list2):
        if i!=j: return False
    return True


def pick_new_points(training_indep, training_dep, testing_data, number_of_objectives, lessismore_status):
    # add new dependent value based on cdom
    transformed_training_dep = get_cdom_values(training_dep, lessismore_status)
    # Build a CART regression tree
    from sklearn.tree import DecisionTreeRegressor
    model = DecisionTreeRegressor(min_samples_leaf=3)
    model = model.fit(training_indep, transformed_training_dep)

    # out = tree.export_graphviz(model, out_file="temp.dot")
    rules, selected_samples = get_rules(model, training_indep, transformed_training_dep)

    compliant_data = get_satisfying_entries(training_indep, testing_data, rules)
    # print "Length of Filtered Data: ", len(compliant_data)
    assert(len(compliant_data) == 1), "Something is wrong"

    return compliant_data

def run_main():
    from utility import read_file, split_data, build_model

    files = [
 # './Data/llvm_input.csv',
 # './Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset1.csv',
 # './Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset2.csv',
 # './Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset1.csv',
 # './Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset2.csv',
 # './Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset1.csv',
 # './Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset2.csv',
 # './Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset1.csv',
 # './Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset2.csv',
 # './Data/noc_CM_log.csv',
 # './Data/POM3A-p10000-d9-o3-dataset1.csv',
 # './Data/POM3A-p10000-d9-o3-dataset2.csv',
 # './Data/POM3B-p10000-d9-o3-dataset1.csv',
 # './Data/POM3B-p10000-d9-o3-dataset2.csv',
 # './Data/POM3C-p10000-d9-o3-dataset1.csv',
 # './Data/POM3C-p10000-d9-o3-dataset2.csv',
 # './Data/POM3D-p10000-d9-o3-dataset1.csv',
 # './Data/POM3D-p10000-d9-o3-dataset2.csv',
 # './Data/rs-6d-c3.csv',
 # './Data/SaC1_2.csv',
 # './Data/SaC_11_12.csv',
 # './Data/SaC_3_4.csv',
 # './Data/SaC_5_6.csv',
 # './Data/SaC_7_8.csv',
 # './Data/SaC_9_10.csv',
 './Data/sort_256.csv',
 # './Data/TriMesh.csv',
 './Data/TriMesh_1_2.csv',
 './Data/TriMesh_2_3.csv',
 './Data/wc+rs-3d-c4.csv',
 './Data/wc+sol-3d-c4.csv',
 './Data/wc+wc-3d-c4.csv',
 './Data/wc-3d-c4.csv',
 './Data/wc-5d-c5.csv',
 './Data/wc-6d-c1.csv',
 './Data/wc-c1-3d-c1.csv',
 './Data/wc-c3-3d-c1.csv',
 # './Data/x264-DB.csv',
 './Data/x264-DB_1_2.csv',
 './Data/x264-DB_2_3.csv',
 './Data/x264-DB_3_4.csv',
 './Data/x264-DB_4_5.csv',
 './Data/x264-DB_5_6.csv',
 './Data/xomo_all-p10000-d27-o4-dataset1.csv',
 './Data/xomo_all-p10000-d27-o4-dataset2.csv',
 './Data/xomo_all-p10000-d27-o4-dataset3.csv',
 './Data/xomo_flight-p10000-d27-o4-dataset1.csv',
 './Data/xomo_flight-p10000-d27-o4-dataset2.csv',
 './Data/xomo_flight-p10000-d27-o4-dataset3.csv',
 './Data/xomo_ground-p10000-d27-o4-dataset1.csv',
 './Data/xomo_ground-p10000-d27-o4-dataset2.csv',
 './Data/xomo_ground-p10000-d27-o4-dataset3.csv',
 './Data/xomo_osp-p10000-d27-o4-dataset1.csv',
 './Data/xomo_osp-p10000-d27-o4-dataset2.csv',
 './Data/xomo_osp-p10000-d27-o4-dataset3.csv',
 './Data/xomoo2-p10000-d27-o4-dataset1.csv',
 './Data/xomoo2-p10000-d27-o4-dataset2.csv',
 './Data/xomoo2-p10000-d27-o4-dataset3.csv']



    all_data = {}
    initial_sample_size = 20
    for file in files:
        all_data[file] = {}
        all_data[file]['evals'] = []
        all_data[file]['gen_dist'] = []
        all_data[file]['igd'] = []

        print file
        data = read_file(file)
        name = file.split('/')[-1][:-4]

        # Creating Objective Dict
        objectives_dict = {}
        for d in data:
            key = ",".join(map(str, d.decisions))
            objectives_dict[key] = d.objectives

        testing_data = [d.decisions for d in data]
        actual_dependent = [objectives_dict[",".join(map(str, d))] for d in testing_data]
        true_pf_indexes = non_dominated_sort_fast(actual_dependent, lessismore[file])
        true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x: x[0])

        for rep in xrange(20):
            print ".| ",
            sys.stdout.flush()
            shuffle(data)

            lives = 10
            training_indep = [d.decisions for d in data[:initial_sample_size]]

            previous_pf = []

            counting_dict = {}
            for d in data:
                key = ",".join(map(str, d.decisions))
                counting_dict[key] = 0

            while True:
                print "# ",
                sys.stdout.flush()
                # Creating Count Dict -- To make sure that if a point is evaluated twice, it is counted as once
                def get_evals():
                    return sum(1 if counting_dict[key] > 0 else 0 for key in counting_dict.keys())

                def get_objective_score(independent):
                    key = ",".join(map(str, independent))
                    counting_dict[key] += 1
                    return objectives_dict[key]

                # print "1. Length of training Data: ", len(training_indep), get_evals()
                training_dep = [get_objective_score(r) for r in training_indep]
                number_of_objectives = len(training_dep[0])

                predicted_pf = pick_new_points(training_indep, training_dep, testing_data, number_of_objectives, lessismore[file])
                actual_dep_predicted_pf = [get_objective_score(r) for r in predicted_pf]
                current_pf_indexes = non_dominated_sort_fast(training_dep + actual_dep_predicted_pf, lessismore[file])
                current_pf = [(training_indep + predicted_pf)[i] for i in current_pf_indexes]

                training_indep = training_indep + predicted_pf

                previously_seen = []
                previously_not_seen = []
                if len(previous_pf) == 0:
                    previous_pf = current_pf
                else:
                    for cr in current_pf:
                        seen = False
                        for pr in previous_pf:
                            # Previously Seen
                            if same_list(pr, cr):
                                seen = True
                                previously_seen.append(cr)
                                continue
                        if seen is False:
                            previously_not_seen.append(cr)
                    previous_pf = previously_seen + previously_not_seen

                    if len(previously_not_seen) == 0:
                        # print "Life Lost"
                        lives -= 1
                if lives == 0: break


            # Calculate the True ND
            training_dependent = [get_objective_score(r) for r in training_indep]
            pf_indexes = non_dominated_sort_fast(training_dependent, lessismore[file])
            current_pf = [training_dependent[i] for i in pf_indexes]
            all_data[file]['evals'].append(get_evals())

            # print
            # print "Evaluations: ", get_evals()

            # actual_dependent = [get_objective_score(d) for d in testing_data]
            # true_pf_indexes = non_dominated_sort_fast(actual_dependent, lessismore[file])
            # true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x: x[0])
            current_pf = sorted(current_pf, key=lambda x: x[0])
            # from utility import draw_pareto_front
            # draw_pareto_front(actual_dependent, true_pf, current_pf)
            all_data[file]['gen_dist'].append(generational_distance(true_pf, current_pf, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(true_pf, current_pf, ranges[file]))
            print
        # raw_input()

        print [round(x, 5) for x in all_data[file]['evals']]
        print [round(x, 5) for x in all_data[file]['gen_dist']]
        print [round(x, 5) for x in all_data[file]['igd']]


        import pickle
        pickle.dump(all_data, open('./FastFlashPickleLocker/' + name + '.p', 'w'))

run_main()