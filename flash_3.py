from __future__ import division
import numpy as np
import os
import sys
from random import shuffle, sample
from utility import lessismore, generational_distance, ranges, inverted_generational_distance, read_file
from non_dominated_sort import non_dominated_sort, binary_domination
import pickle


def run_flash3(files, repeat_no):
    all_data = {}
    n0 = 20
    n1 = 256

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


        true_pf_dependent = [d.objectives for d in data]
        true_pf_indexes = non_dominated_sort(true_pf_dependent, lessismore[file])
        true_pf = sorted([true_pf_dependent[i] for i in true_pf_indexes], key=lambda x: x[0])

        no_objectives = len(data[0].objectives)
        evals = []
        pfs = []
        for rep in xrange(1):
            print ". ",
            sys.stdout.flush()
            shuffle(data)

            lives = 10
            training_indep = [d.decisions for d in data[:n0]]
            testing_indep = [d.decisions for d in data[n0:]]
            evaluation_count = 0
            previous_pf = []

            counting_dict = {}
            for d in data:
                key = ",".join(map(str, d.decisions))
                counting_dict[key] = 0

            iteration_count = 0
            while True:
                # Creating Count Dict -- To make sure that if a point is evaluated twice, it is counted as once
                print ". ",
                def get_objective_score(independent):
                    key = ",".join(map(str, independent))
                    # print "@@ ", counting_dict[key]
                    counting_dict[key] += 1
                    # print "@@| ", counting_dict[key]
                    return objectives_dict[key]


                training_dep = [get_objective_score(r) for r in training_indep]

                n1_select = testing_indep[n0 + iteration_count * n1: n0 + (iteration_count + 1) * n1]

                # build CART Trees for each objective
                models = []
                predictions = []
                for obj_no in xrange(no_objectives):
                    from sklearn.tree import DecisionTreeRegressor
                    temp_model = DecisionTreeRegressor()
                    temp_model.fit(training_indep, [t[obj_no] for t in training_dep])
                    predictions.append(temp_model.predict(n1_select))
                    models.append(temp_model)

                assert(len(predictions) == no_objectives), "Something is wrong"
                assert(len(predictions[0]) == len(predictions[1])), "Something is wrong"

                # Merge the predictions together
                merged_predictions = []
                for i in xrange(len(predictions[0])):
                    merged_predictions.append([predictions[obj_no][i] for obj_no in xrange(len(predictions))])

                # Choose the dominating points from merged predictions
                merged_indexes = non_dominated_sort(merged_predictions, lessismore[file])
                predicted_few = [merged_predictions[i] for i in merged_indexes]

                selected_n1 = []
                for predicted_f in predicted_few:
                    for train_dep in training_dep:
                        if binary_domination(train_dep, predicted_f) is False:
                            selected_n1.append(n1_select[i])

                # removing duplicate entries
                import itertools
                selected_n1.sort()
                selected_n1 = list(k for k, _ in itertools.groupby(selected_n1))

                print "Length of selected_n1: ", len(selected_n1), get_evals()
                assert(len(selected_n1) < n1), "Somethign is wrong"
                if len(selected_n1) == 0:
                    lives -= 1
                    # print "Life lost"
                else:
                    training_indep += selected_n1

                if lives == 0 or n0 + (iteration_count + 1) * n1 > len(data): break
                iteration_count += 1
            print

            # print "Size of the frontier = ", len(training_indep), " Evals: ", get_evals()
            # Calculate the True ND
            training_dependent = [get_objective_score(r) for r in training_indep]
            current_pf_indexes = non_dominated_sort(training_dependent, lessismore[file])
            current_pf = [training_dependent[i] for i in current_pf_indexes]
            current_pf = sorted(current_pf, key=lambda x: x[0])

            all_data[file]['evals'].append(get_evals())
            all_data[file]['gen_dist'].append(generational_distance(true_pf, current_pf, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(true_pf, current_pf, ranges[file]))

        print "Evals: ",  all_data[file]['evals']
        print "GD: ",  all_data[file]['gen_dist']
        print "IGD: ", all_data[file]['igd']

        pickle.dump(all_data, open('Flash3_Data/PickleLocker/' + file.split('/')[-1][:-4] + "_" + str(repeat_no) + ".p", "w"))

def run_main():
    files = [
                './Data/llvm_input.csv',
                './Data/noc_CM_log.csv',
                './Data/sort_256.csv',
                './Data/wc+rs-3d-c4.csv',
                './Data/wc+sol-3d-c4.csv',
                './Data/wc+wc-3d-c4.csv',
                './Data/wc-3d-c4.csv',
                './Data/wc-5d-c5.csv',
                './Data/wc-6d-c1.csv',
                './Data/wc-c1-3d-c1.csv',
                './Data/wc-c3-3d-c1.csv',
                './Data/rs-6d-c3.csv',
                './Data/MONRP_50_4_5_0_110.csv',
                './Data/MONRP_50_4_5_0_90.csv',
                './Data/MONRP_50_4_5_4_110.csv',
                './Data/MONRP_50_4_5_4_90.csv',
                './Data/POM3A.csv',
                './Data/POM3B.csv',
                './Data/POM3C.csv',
                './Data/POM3D.csv',
                './Data/xomo_all.csv',
                './Data/xomo_flight.csv',
                './Data/xomo_ground.csv',
                './Data/xomo_osp.csv',
                './Data/xomoo2.csv'
             ]

    import multiprocessing as mp

    # Main control loop
    pool = mp.Pool()
    for file in files:
        for rep in xrange(20):
            # print file, rep
            pool.apply_async(run_flash3, ([file], rep))
            # run_flash3([file], rep)

    pool.close()
    pool.join()


if __name__ == "__main__":
    run_main()


