from __future__ import division
import numpy as np
import os
import sys
from random import shuffle
from utility import lessismore, generational_distance, ranges, inverted_generational_distance
from non_dominated_sort import non_dominated_sort, binary_domination
import math


def get_nd_solutions(filename, training_indep, training_dep, testing_indep):
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
    for i, j in zip(predicted_objectives[0], predicted_objectives[1]):
        merged_predicted_objectves.append([i, j])
    assert(len(merged_predicted_objectves) == len(predicted_objectives[0])), "Something is wrong"

    # Find Non-Dominated Solutions
    pf_indexes = non_dominated_sort(merged_predicted_objectves, lessismore[filename], [r[0] for r in ranges], [r[1] for r in ranges])
    # print "Number of ND Solutions: ", len(pf_indexes)

    return [testing_indep[i] for i in pf_indexes], [merged_predicted_objectves[i] for i in pf_indexes]


def get_next_point(file, training_indep, training_dep, testing_indep):
    def euclidean_distance(rlist1, rlist2):
        assert(len(rlist1) == len(rlist2)), "The points don't have the same dimension"
        distance = sum([(i - j) ** 2 for i, j in zip(rlist1, rlist2)])
        assert(distance >= 0), "Distance can't be less than 0"
        return distance

    # print len(testing_indep)
    no_of_objectives = len(training_dep[0])
    # First level of filter
    # build a model and get the predicted non dominated solutions
    returned_nd_independent, predicted_objectives = get_nd_solutions(file, training_indep, training_dep, testing_indep)

    # Find solutions not in the training set (training_indep)
    indeps = []
    deps = []
    for i, rni in enumerate(returned_nd_independent):
        if rni not in training_indep:
            indeps.append(rni)
            deps.append(predicted_objectives[i])

    assert(len(indeps) <= len(returned_nd_independent)), "Something is wrong"

    if len(deps) == 0:
        indexes = range(len(testing_indep))
        for index in indexes:
            if testing_indep[index] not in training_indep:
                return testing_indep[index]

    # TODO len(indep) is 0. Everything that is good has been previously seen

    # TODO Find the predicted values of training_indep. This is to make sure that selected far away from the seen points

    # Normalized the objective space of deps
    normalized_deps = []
    for dep in deps:
        # Since distance is measured in the objective space, the distances need to be normalized
        temp = []
        for noo in xrange(no_of_objectives):
            temp.append((dep[noo] - ranges[file][noo][0]) / (ranges[file][noo][1] - ranges[file][noo][0]))
        assert (len(temp) == len(dep)), "Something is wrong"
        normalized_deps.append(temp)
    assert(len(deps) == len(normalized_deps)), "Something is wrong"

    # Normalized the objective space of training_dep
    normalized_training_deps = []
    for ti in training_dep:
        temp = []
        for noo in xrange(no_of_objectives):
            temp.append((ti[noo] - ranges[file][noo][0]) / (ranges[file][noo][1] - ranges[file][noo][0]))
        assert (len(temp) == len(ti)), "Something is wrong"
        normalized_training_deps.append(temp)
    assert(len(normalized_training_deps) == len(training_dep)), "Something is wrong"

    # Find the point furthest away from training_dep
    distance_dep = []
    for ndep in normalized_deps:
        distance_dep.append(np.mean([euclidean_distance(ndep, ntd) for ntd in normalized_training_deps]))

    if len(distance_dep) == 0: return
    # Find point with the largest distance
    max_index = distance_dep.index(max(distance_dep))
    # assert(indeps[max_index] in training_indep is False), "Something is wrong"
    if indeps[max_index] in training_indep is True:
        import pdb
        pdb.set_trace()
    return indeps[max_index]


if __name__ == "__main__":
    from utility import read_file, split_data, build_model
    files = ['./Data/llvm_input.csv', './Data/noc_CM_log.csv',
              './Data/sort_256.csv',
             './Data/wc+rs-3d-c4.csv', './Data/wc+sol-3d-c4.csv', './Data/wc+wc-3d-c4.csv',
             './Data/wc-3d-c4.csv', './Data/wc-5d-c5.csv', './Data/wc-6d-c1.csv', './Data/wc-c1-3d-c1.csv',
             './Data/wc-c3-3d-c1.csv', './Data/rs-6d-c3.csv']

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
        for rep in xrange(20):
            print ". ",
            sys.stdout.flush()
            shuffle(data)

            lives = 10
            training_indep = [d.decisions for d in data[:initial_sample_size]]
            testing_indep = [d.decisions for d in data]
            evaluation_count = 0
            previous_pf = []

            counting_dict = {}
            for d in data:
                key = ",".join(map(str, d.decisions))
                counting_dict[key] = 0

            count = 0
            step_size = 128
            while True:
                sys.stdout.flush()

                def get_objective_score(independent):
                    key = ",".join(map(str, independent))
                    # print independent, counting_dict[key]
                    counting_dict[key] += 1
                    return objectives_dict[key]

                training_dep = [get_objective_score(r) for r in training_indep]

                # to make sure right part of testing_indep is passed to get_next_point
                if (count+1) * step_size > len(testing_indep):
                    start = count * step_size
                    end = len(testing_indep)
                    count = 0
                else:
                    start = count * step_size
                    end = (count+1) * step_size
                    count += 1

                next_point = get_next_point(file, training_indep, training_dep, testing_indep[start:end])
                if next_point is None: continue
                # assert(counting_dict[",".join(map(str, next_point))] == 0), "Something is wrong"
                if counting_dict[",".join(map(str, next_point))] != 0:
                    import pdb
                    pdb.set_trace()
                next_point_dependent = get_objective_score(next_point)

                # Check if next_point is dominated by other sampled points (training_dep)
                for td in training_dep:
                    if binary_domination(td, next_point_dependent) is True:
                        # td dominated next_point_dependent
                        lives -= 1
                        break

                # Adding next_point to training_indep
                training_indep = training_indep + [next_point]
                if lives == 0: break

            print "Size of the frontier = ", len(training_indep), " Evals: ", get_evals(),
            # Calculate the True ND
            training_dependent = [get_objective_score(r) for r in training_indep]
            pf_indexes = non_dominated_sort(training_dependent, lessismore[file], [r[0] for r in ranges[file]], [r[1] for r in ranges[file]])
            current_pf = [training_dependent[i] for i in pf_indexes]
            all_data[file]['evals'].append(get_evals())

            actual_dependent = [get_objective_score(d) for d in testing_indep]
            true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file], [r[0] for r in ranges[file]], [r[1] for r in ranges[file]])
            true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])
            current_pf = sorted(current_pf, key=lambda x:x[0])
            from utility import draw_pareto_front
            # draw_pareto_front(actual_dependent, true_pf, current_pf)
            all_data[file]['gen_dist'].append(generational_distance(true_pf, current_pf, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(true_pf, current_pf, ranges[file]))

            print " GD: ",  all_data[file]['gen_dist'][-1],
            print " IGD: ",  all_data[file]['igd'][-1]

        print [round(x, 5) for x in all_data[file]['evals']]
        print [round(x, 5) for x in all_data[file]['gen_dist']]
        print [round(x, 5) for x in all_data[file]['igd']]


    import pickle
    pickle.dump(all_data, open('al-based-4.p', 'w'))
