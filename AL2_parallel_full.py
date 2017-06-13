from __future__ import division
import numpy as np
import os
import sys
from random import shuffle
from utility import lessismore, generational_distance, ranges, inverted_generational_distance
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


def get_nd_solutions(filename, train_indep, training_dep, testing_indep, mins, maxs):
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
    pf_indexes = non_dominated_sort(merged_predicted_objectves, lessismore[filename], mins, maxs)
    # print "Number of ND Solutions: ", len(pf_indexes)

    return [testing_indep[i] for i in pf_indexes], [merged_predicted_objectves[i] for i in pf_indexes]


def same_list(list1, list2):
    assert(len(list1) == len(list2)), "Something is wrong"
    for i, j in zip(list1, list2):
        if i!=j: return False
    return True


def get_training_sequence(file, training_indep, training_dep, testing_data, mins, maxs):
    # build a model and get the predicted non dominated solutions
    return_nd_independent, predicted_objectives = get_nd_solutions(file, training_indep, training_dep, testing_data, mins, maxs)
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

def run_main(files, repeat_no):
    print files, repeat_no
    from utility import read_file, split_data, build_model
    # files = ['./Data/llvm_input.csv', './Data/noc_CM_log.csv',
    #           './Data/sort_256.csv',
    #          './Data/wc+rs-3d-c4.csv', './Data/wc+sol-3d-c4.csv', './Data/wc+wc-3d-c4.csv',
    #          './Data/wc-3d-c4.csv', './Data/wc-5d-c5.csv', './Data/wc-6d-c1.csv', './Data/wc-c1-3d-c1.csv',
    #          './Data/wc-c3-3d-c1.csv', './Data/rs-6d-c3.csv']
    import os
    print "Working in Process #%d" % (os.getpid())
    all_data = {}
    initial_sample_size = 30
    for file in files:
        all_data[file] = {}
        all_data[file]['evals'] = []
        all_data[file]['gen_dist'] = []
        all_data[file]['igd'] = []

        mins = [r[0] for r in ranges[file]]
        maxs = [r[1] for r in ranges[file]]

        print file
        data = read_file(file)

        # Creating Objective Dict
        objectives_dict = {}

        for d in data:
            key = ",".join(map(str, d.decisions))
            objectives_dict[key] = d.objectives

        evals = []
        pfs = []
        for rep in xrange(1):
            print ". ",
            sys.stdout.flush()
            shuffle(data)

            lives = 20
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
                print os.getpid(), len(training_data)

                def get_evals():
                    return sum(1 if counting_dict[key]>0 else 0 for key in counting_dict.keys())

                def get_objective_score(independent):
                    key = ",".join(map(str, independent))
                    # print "@@ ", counting_dict[key]
                    counting_dict[key] += 1
                    # print "@@| ", counting_dict[key]
                    return objectives_dict[key]


                training_dep = [get_objective_score(r) for r in training_data]

                training_sequence, return_nd_independent = get_training_sequence(file, training_data, training_dep, testing_data, mins, maxs)
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
                before_pf_indexes = non_dominated_sort(training_dep, lessismore[file], mins, maxs)
                before_pf = [training_dep[i] for i in before_pf_indexes]

                training_data = training_data + [next_point]

                after_pf_indexes = non_dominated_sort(training_dep + [next_point_dependent], lessismore[file], mins, maxs)
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
                import itertools
                training_data.sort()
                training_data = [k for k, _ in itertools.groupby(training_data)]

                if lives == 0: break

            print "Size of the frontier = ", len(training_data), " Evals: ", get_evals(),
            # Calculate the True ND
            training_dependent = [get_objective_score(r) for r in training_data]
            assert(len(training_data) == len(training_dependent)), "Something is wrong"
            collected_content = []
            for t_indep, t_dep in zip(training_data, training_dependent):
                collected_content += [t_indep + t_dep]

            name = files[-1].split('/')[-1][:-4]
            filename_store = "./Flash_Collector/" + name + "_" + str(repeat_no) + ".csv"

            f = open(filename_store, 'w')
            for cc in collected_content:
                temp = ",".join(map(str, cc)) + '\n'
                f.write(temp)
            f.close()

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

    # Main control loop
    pool = mp.Pool()
    for file in files:
        for rep in xrange(20):
            pool.apply_async(run_main, ([file], rep))
            # run_main([file], rep)

    pool.close()
    pool.join()
