from __future__ import division

import numpy as np

import os

import sys

from random import shuffle

from utility import lessismore, generational_distance, ranges

from non_dominated_sort import non_dominated_sort







def policy1(scores, lives=3):

        """

        no improvement in last 4 runs

        """

        status = [False, False]

        objectives_no = len(scores[0])

        for objective_no in xrange(objectives_no):

            temp_lives = lives

            last = scores[0][objective_no]

            for i,score in enumerate(scores):

                if i > 0:

                    if temp_lives == 0:

                        status[objective_no] = True

                    elif score[objective_no] >= last:

                        temp_lives -= 1

                        last = score[objective_no]

                    else:

                        temp_lives = lives

                        last = score[objective_no]

        # print len(scores), status

        if all(status) is True: return True

        else: return False





def rank_progressive(train_independent, train_dependent, validation_independent, validation_dependent):

    # Note that we do not use the validation dependent since the validation data is presorted

    from sklearn.tree import DecisionTreeRegressor

    model = DecisionTreeRegressor()

    model.fit(train_independent, train_dependent)

    predicted = model.predict(validation_independent)

    # assigning actual rank, since validation datasets are already sorted

    actual_validation_order = [[i,p] for i,p in enumerate(predicted)]

    predicted_sorted = sorted(actual_validation_order, key=lambda x: x[-1])

    # assigning predicted ranks

    predicted_rank_sorted = [[p[0], p[-1], i] for i,p in enumerate(predicted_sorted)]

    rank_diffs = [abs(p[0] - p[-1]) for p in predicted_rank_sorted]

    return np.mean(rank_diffs)





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



    return [testing_indep[i] for i in pf_indexes][:10]



def same_list(list1, list2):

    assert(len(list1) == len(list2)), "Something is wrong"

    for i, j in zip(list1, list2):

        if i!=j: return False

    return True



if __name__ == "__main__":

    from utility import read_file, split_data, build_model

    files = ['./Data/reduced_SaC_5_6.csv']



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

            # Creating Count Dict -- To make sure that if a point is evaluated twice, it is counted as once

            counting_dict = {}

            for d in data:

                key = ",".join(map(str, d.decisions))

                counting_dict[key] = 0



            def get_evals():

                return sum(1 if counting_dict[key]>0 else 0 for key in counting_dict.keys())



            def get_objective_score(independent):

                key = ",".join(map(str, independent))

                counting_dict[key] += 1

                return objectives_dict[key]



            print "#  ",

            sys.stdout.flush()

            shuffle(data)



            lives = 1

            training_data = [d.decisions for d in data[:initial_sample_size]]

            testing_data = [d.decisions for d in data]

            evaluation_count = 0

            previous_pf = []

            while True:

                print ". ",

                sys.stdout.flush()

                # print "Length of training Data: ", len(training_data)

                training_dep = [get_objective_score(r) for r in training_data]

                return_nd_independent = get_nd_solutions(file, training_data, training_dep, testing_data)

                # Evaluate predicted pareto front

                return_actual_dependent_values = [get_objective_score(r) for r in return_nd_independent]



                # Get Actual Pareto Front --- Size of Predicted PF >> Size of Actual PF

                current_pf_indexes = non_dominated_sort(return_actual_dependent_values, lessismore[file])

                current_pf = [return_nd_independent[i] for i in current_pf_indexes]



                training_data = training_data + return_nd_independent



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

            print



            # print "Number of Evaluations = ", get_evals()

            # Calculate the True ND

            training_dependent = [get_objective_score(r) for r in training_data]

            pf_indexes = non_dominated_sort(training_dependent, lessismore[file])

            current_pf = [training_dependent[i] for i in pf_indexes]

            print "Size of the frontier = ", len(current_pf), " Evals: ", get_evals()

            pfs.append(current_pf)

            evals.append(get_evals())

            all_data[file]['evals'].append(get_evals())





            actual_dependent = [get_objective_score(d) for d in testing_data]

            true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file])

            true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])

            current_pf = sorted(current_pf, key=lambda x:x[0])

            from utility import draw_pareto_front

            # draw_pareto_front(actual_dependent, true_pf, current_pf)

            all_data[file]['gen_dist'].append(generational_distance(true_pf, current_pf, ranges[file]))





    import pickle

    pickle.dump(all_data, open('al-reduced_SaC_5_6.p', 'w'))

