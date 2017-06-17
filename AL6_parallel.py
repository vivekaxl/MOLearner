from __future__ import division
import numpy as np
import os
import sys
from random import shuffle
from utility import lessismore, generational_distance, ranges, inverted_generational_distance, read_file
from non_dominated_sort import non_dominated_sort, binary_domination


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
    for i in xrange(len(predicted_objectives[0])):
        merged_predicted_objectves.append([predicted_objectives[obj_no][i] for obj_no in xrange(no_of_objectives)])
    assert(len(merged_predicted_objectves) == len(testing_indep)), "Something is wrong"

    # Find Non-Dominated Solutions
    pf_indexes = non_dominated_sort(merged_predicted_objectves, lessismore[filename], [r[0] for r in ranges], [r[1] for r in ranges])
    # print "Number of ND Solutions: ", len(pf_indexes)

    return [testing_indep[i] for i in pf_indexes], [merged_predicted_objectves[i] for i in pf_indexes]

def normalize(x, min, max):
    tmp = float((x - min)) / (max - min + 0.000001)
    if tmp > 1: return 1
    elif tmp < 0: return 0
    else: return tmp


def get_next_points(file, training_indep, training_dep, testing_indep, directions):
    no_of_objectives = len(training_dep[0])

    predicted_objectives = []
    for objective_no in xrange(no_of_objectives):
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        model.fit(training_indep, [t[objective_no] for t in training_dep])
        predicted = model.predict(testing_indep)
        predicted_objectives.append(predicted)

    # Merge the objectives
    merged_predicted_objectves = []
    for i in xrange(len(predicted_objectives[0])):
        merged_predicted_objectves.append([predicted_objectives[obj_no][i] for obj_no in xrange(no_of_objectives)])
    assert (len(merged_predicted_objectves) == len(testing_indep)), "Something is wrong"


    # Convert the merged_predicted_objectives to minimization problem
    lism = lessismore[file]
    dependents = []
    for rd in merged_predicted_objectves:
        temp = []
        for i in xrange(len(lism)):
            # if lessismore[i] is true - Minimization else Maximization
            if lism[i] is False:
                temp.append(-1 * rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    # Normalize objectives
    mins = [r[0] for r in ranges[file]]
    maxs = [r[1] for r in ranges[file]]

    normalized_dependents = []
    for dependent in dependents:
        normalized_dependents.append([normalize(dependent[i], mins[i], maxs[i]) for i in xrange(no_of_objectives)])
    assert(len(normalized_dependents) == len(dependents)), "Something is wrong"

    return_indexes = []
    for direction in directions:
        transformed = []
        for dependent in normalized_dependents:
            assert(len(direction) == len(dependent)), "Something is wrong"
            transformed.append(sum([i*j for i, j in zip(direction, dependent)]))
        return_indexes.append(transformed.index(min(transformed)))
    assert(len(return_indexes) == len(directions)), "Something is wrong"

    return_indexes = list(set(return_indexes))
    return return_indexes



def get_random_numbers(len_of_objectives):
    from random import random
    random_numbers = [random() for _ in xrange(len_of_objectives)]
    ret = [num/sum(random_numbers) for num in random_numbers]
    print ret, sum(ret), int(sum(ret))==1
    # assert(int(sum(ret)) == 1), "Something is wrong"
    return ret


def run_main(files, repeat_no):
    print files, repeat_no
    all_data = {}
    initial_sample_size = 10
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
            return sum(1 if counting_dict[key] > 0 else 0 for key in counting_dict.keys())

        number_of_objectives = len(data[0].objectives)
        number_of_directions = 10

        directions = [get_random_numbers(number_of_objectives) for _ in xrange(number_of_directions)]

        for rep in xrange(20):
            shuffle(data)

            training_indep = [d.decisions for d in data[:initial_sample_size]]
            testing_indep = [d.decisions for d in data[initial_sample_size:]]

            counting_dict = {}
            for d in data:
                key = ",".join(map(str, d.decisions))
                counting_dict[key] = 0

            while True:
                print ". ",
                sys.stdout.flush()

                def get_objective_score(independent):
                    key = ",".join(map(str, independent))
                    # print independent, counting_dict[key]
                    counting_dict[key] += 1
                    return objectives_dict[key]

                training_dep = [get_objective_score(r) for r in training_indep]

                next_point_indexes = get_next_points(file, training_indep, training_dep, testing_indep, directions)
                print "Points Sampled: ", next_point_indexes
                next_point_indexes = sorted(next_point_indexes, reverse=True)
                next_points = [testing_indep[npi] for npi in next_point_indexes]
                for next_point_index in next_point_indexes:
                    temp = testing_indep[next_point_index]
                    del testing_indep[next_point_index]
                    training_indep.append(temp)
                print len(training_indep), len(testing_indep), len(data)
                assert(len(training_indep) + len(testing_indep) == len(data)), "Something is wrong"
                if len(training_indep) > 50: break

            print "Size of the frontier = ", len(training_indep), " Evals: ", get_evals(),
            # Calculate the True ND
            training_dependent = [get_objective_score(r) for r in training_indep]
            all_data[file]['evals'].append(get_evals())

            actual_dependent = [get_objective_score(d) for d in testing_indep]
            true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file], [r[0] for r in ranges[file]],
                                                 [r[1] for r in ranges[file]])
            true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x: x[0])
            print "Length of True PF: " , len(true_pf)
            print "Length of the Actual PF: ", len(training_dependent)
            all_data[file]['gen_dist'].append(generational_distance(true_pf, training_dependent, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(true_pf, training_dependent, ranges[file]))

            print " GD: ", all_data[file]['gen_dist'][-1],
            print " IGD: ", all_data[file]['igd'][-1]

        print [round(x, 5) for x in all_data[file]['evals']]
        print [round(x, 5) for x in all_data[file]['gen_dist']]
        print [round(x, 5) for x in all_data[file]['igd']]

        import pickle
        pickle.dump(all_data, open('AL6_PickleLocker/AL6_'+ file.split('/')[-1][:-4] + '_' + str(repeat_no) +'.p', 'w'))

if __name__ == "__main__":
    files = [
        './Data/POM3A.csv',
        './Data/POM3B.csv',
        './Data/POM3C.csv',
        './Data/POM3D.csv', './Data/xomo_all.csv',
        './Data/xomo_flight.csv',
        './Data/xomo_ground.csv',
        './Data/xomo_osp.csv',
        './Data/xomoo2.csv','./Data/xomo_all.csv',
        './Data/MONRP_50_4_5_0_110.csv',
        './Data/MONRP_50_4_5_0_90.csv',
        './Data/MONRP_50_4_5_4_110.csv',
        './Data/MONRP_50_4_5_4_90.csv',

    ]

    import multiprocessing as mp
    from time import time

    times = {}
    # Main control loop
    pool = mp.Pool()
    for file in files:
        times[file] = []
        for rep in xrange(20):
            # pool.apply_async(run_main, ([file], rep))
            start_time = time()
            run_main([file], rep)
            times[file].append(time() - start_time)
    import pickle
    pickle.dump(times, open('AL6_times.p', 'w'))

    pool.close()
    pool.join()

