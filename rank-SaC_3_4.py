from __future__ import division

import numpy as np

import os

import sys

from utility import lessismore

from utility import draw_pareto_front, generational_distance, ranges,inverted_generational_distance







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





def rank_based_approach(training_data, testing_data):

    # Setting up for rank progressive

    initial_size = 10

    sub_train = [training_indep for training_indep in training_data[:initial_size]]



    steps = 0

    rank_diffs = []

    while (initial_size+steps) < len(training_data) - 1:

        no_of_objectives = len(sub_train[0].objectives)

        sub_train_indep = [s.decisions for s in sub_train]

        testing_indep = [s.decisions for s in testing_data]

        mean_rank_diff = []

        for objective_no in xrange(no_of_objectives):

            sub_train_dep = [s.objectives[objective_no] for s in sub_train]

            testing_dep = [s.objectives[objective_no] for s in testing_data]

            mean_rank_diff.append(rank_progressive(sub_train_indep, sub_train_dep, testing_indep, testing_dep))



        rank_diffs.append(mean_rank_diff)

        policy_result = policy1(rank_diffs)

        if policy_result is True : break

        steps += 1

        sub_train.append(training_data[initial_size+steps])

    return sub_train



if __name__ == "__main__":

    from utility import read_file, split_data, build_model

    from non_dominated_sort import non_dominated_sort

    files = ['./Data/SaC_3_4.csv']





    all_data = {}

    for file in files:

        all_data[file] = {}

        all_data[file]['evals'] = []

        all_data[file]['gen_dist'] = []

        all_data[file]['igd'] = []



        print file

        data = read_file(file)

        for rep in xrange(20):

            print ". ",

            sys.stdout.flush()

            splits = split_data(data, 40, 2, 58)

            temp = rank_based_approach(splits[0], splits[1])



            predicted_dependent = build_model(temp, splits[2])



            actual_dependent = [d.objectives for d in splits[2]]



            true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file])

            predicted_pf_indexes = non_dominated_sort(predicted_dependent, lessismore[file])

            # Actual Dependent values of the predicted_pf

            predicted_actual =[actual_dependent[i] for i in predicted_pf_indexes]

            # As an additional filter and second round of non-dominated sorting is performed == No additional evaluations

            filtered_predicted_pf_index = non_dominated_sort(predicted_actual, lessismore[file])



            true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])

            predicted_pf = sorted([predicted_actual[i] for i in filtered_predicted_pf_index], key=lambda x:x[0])

            # predicted_pf = sorted([actual_dependent[i] for i in predicted_pf_indexes], key=lambda x:x[0])



            # draw_pareto_front(actual_dependent, true_pf, predicted_pf, filename=file.split('/')[-1] + "_" + str(rep))

            # print "Length of Training set: ", len(temp)

            # print "Length of Validation set: ", len(splits[1])

            # print "Generation Distance: ", generational_distance(true_pf, predicted_pf)

            all_data[file]['evals'].append(len(temp) + len(splits[1]))

            all_data[file]['gen_dist'].append(generational_distance(true_pf, predicted_pf, ranges[file]))

            all_data[file]['igd'].append(inverted_generational_distance(true_pf, predicted_pf, ranges[file]))

        print

        print [round(x, 5) for x in all_data[file]['evals']]

        print [round(x, 5) for x in all_data[file]['gen_dist']]

        print [round(x, 5) for x in all_data[file]['igd']]



        import pickle



        pickle.dump(all_data, open('rank-based_' + file.split('/')[-1][:-4] + '.p', 'w'))

