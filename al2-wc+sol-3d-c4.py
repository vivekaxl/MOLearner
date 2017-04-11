from __future__ import division

import numpy as np

import os

import sys

from random import shuffle

from utility import lessismore, generational_distance, ranges

from non_dominated_sort import non_dominated_sort

import math



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



if __name__ == "__main__":

    from utility import read_file, split_data, build_model

    files = ['./Data/wc+sol-3d-c4.csv']



    all_data = {}

    initial_sample_size = 20

    for file in files:

        all_data[file] = {}

        all_data[file]['evals'] = []

        all_data[file]['gen_dist'] = []



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

        for rep in xrange(20):

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



                print "Length of training Data: ", len(training_data), get_evals()

                training_dep = [get_objective_score(r) for r in training_data]



                training_sequence, return_nd_independent = get_training_sequence(file, training_data, training_dep, testing_data)

                assert(len(training_sequence) == len(return_nd_independent)), "Soemthing is wrong"

                next_point = testing_data[training_sequence[0]]

                count = 1

                while not_in_cache(next_point, training_data) is False and count < len(training_sequence):

                    next_point = return_nd_independent[training_sequence[count]]

                    count += 1

                    print "# ", #next_point

                    sys.stdout.flush()



                print

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



                if lives == 0: break



            # Calculate the True ND

            training_dependent = [get_objective_score(r) for r in training_data]

            pf_indexes = non_dominated_sort(training_dependent, lessismore[file])

            current_pf = [training_dependent[i] for i in pf_indexes]

            print "Size of the frontier = ", len(current_pf), " Evals: ", get_evals()

            all_data[file]['evals'].append(get_evals())



            actual_dependent = [get_objective_score(d) for d in testing_data]

            true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file])

            true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])

            current_pf = sorted(current_pf, key=lambda x:x[0])

            from utility import draw_pareto_front

            # draw_pareto_front(actual_dependent, true_pf, current_pf)

            all_data[file]['gen_dist'].append(generational_distance(true_pf, current_pf, ranges[file]))





    import pickle

    pickle.dump(all_data, open('al2-wc+sol-3d-c4.p', 'w'))

