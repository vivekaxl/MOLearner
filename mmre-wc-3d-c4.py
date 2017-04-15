from __future__ import division

import numpy as np

from sklearn.tree import DecisionTreeRegressor

import sys

from utility import draw_pareto_front, generational_distance, ranges,inverted_generational_distance

from non_dominated_sort_fast import non_dominated_sort_fast



def policy(scores, threshold):

    """

    no improvement in last 4 runs

    """

    objectives_no = len(scores)

    status = [False if scores[objective_no] > threshold else True for objective_no in xrange(objectives_no)]

    if all(status) is True: return True

    else: return False





def mmre_progressive(train_independent, train_dependent, validation_independent, validation_dependent):

    model = DecisionTreeRegressor()

    model.fit(train_independent, train_dependent)

    predicted = model.predict(validation_independent)

    mre = []

    for org, pred in zip(validation_dependent, predicted):

        if org == 0: continue

        mre.append(abs(org - pred)/ abs(org))

    return np.mean(mre) * 100





def mmre_based_approach(training_data, testing_data, threshold=5):

    # Setting up for rank progressive

    initial_size = 10

    sub_train = [training_indep for training_indep in training_data[:initial_size]]



    steps = 0

    while (initial_size+steps) < len(training_data) - 1:

        no_of_objectives = len(sub_train[0].objectives)

        sub_train_indep = [s.decisions for s in sub_train]

        testing_indep = [s.decisions for s in testing_data]

        mean_rank_diff = []

        for objective_no in xrange(no_of_objectives):

            sub_train_dep = [s.objectives[objective_no] for s in sub_train]

            testing_dep = [s.objectives[objective_no] for s in testing_data]

            mean_rank_diff.append(mmre_progressive(sub_train_indep, sub_train_dep, testing_indep, testing_dep))



        policy_result = policy(mean_rank_diff, threshold)

        if policy_result is True : break

        steps += 1

        sub_train.append(training_data[initial_size+steps])

    return sub_train



if __name__ == "__main__":

    from utility import read_file, split_data, build_model, lessismore



    files = ['./Data/wc-3d-c4.csv']



    all_data = {}

    for file in files:

        all_data[file] = {}

        all_data[file]['evals'] = []

        all_data[file]['gen_dist'] = []

        all_data[file]['igd'] = []



        print file

        for _ in xrange(20):

            print ". ",

            sys.stdout.flush()

            data = read_file(file)

            splits = split_data(data, 40, 2, 58)

            temp = mmre_based_approach(splits[0], splits[1])



            predicted_dependent = build_model(temp, splits[2])



            actual_dependent = [d.objectives for d in splits[2]]



            true_pf_indexes = non_dominated_sort_fast(actual_dependent, lessismore[file])

            predicted_pf_indexes = non_dominated_sort_fast(predicted_dependent, lessismore[file])

            # Actual Dependent values of the predicted_pf

            predicted_actual =[actual_dependent[i] for i in predicted_pf_indexes]

            # As an additional filter and second round of non-dominated sorting is performed == No additional evaluations

            filtered_predicted_pf_index = non_dominated_sort_fast(predicted_actual, lessismore[file])



            true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])

            # predicted_pf = sorted([predicted_actual[i] for i in filtered_predicted_pf_index], key=lambda x:x[0])

            predicted_pf = sorted([actual_dependent[i] for i in predicted_pf_indexes], key=lambda x:x[0])



            # draw_pareto_front(actual_dependent, true_pf, predicted_pf) #, filename=file.split('/')[-1])

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

        pickle.dump(all_data, open('mmre-based_' + file.split('/')[-1][:-4] + '.p', 'w'))





