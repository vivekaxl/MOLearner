from __future__ import division
import numpy as np
from utility import data_point


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
        print len(scores), status
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


def loss(x1, x2, mins=None, maxs=None):
    from math import exp

    def normalize(x, min, max):
        tmp = float((x - min)) / (max - min)
        return tmp

    # normalize if mins and maxs are given
    if mins and maxs:
        x1 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x1)]
        x2 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x2)]

    o = min(len(x1), len(x2))  # len of x1 and x2 should be equal
    return sum([exp((x2i - x1i) / o) for x1i, x2i in zip(x1, x2)]) / o


def domination(x1, x2, mins, maxs):
    westLoss = loss(x1, x2, mins, maxs)
    eastLoss = loss(x2, x1, mins, maxs)
    EPSILON = 1.0
    # print "West Loss: ", westLoss
    # print "East Loss: ", eastLoss
    if westLoss < EPSILON * eastLoss:
        return westLoss
    return 0


def build_regressor(train, test):
    train_independent = [t.decisions for t in train]
    train_dependent = [t.objectives for t in train]
    test_independent = [t.decisions for t in test]
    test_dependent = [t.objectives for t in test]
    from sklearn.tree import DecisionTreeRegressor
    model = DecisionTreeRegressor()
    model.fit(train_independent, train_dependent)
    predicted = model.predict(test_independent)
    # import pdb
    # pdb.set_trace()
    # abs_diff = 0
    # for i, j in zip(test_dependent, predicted):
    #     abs_diff += abs(i-j)
    #     print abs_diff
    return predicted


def rank_based_approach(training_data, testing_data, mins=None, maxs=None):
    # Setting up for rank progressive
    initial_size = 10
    sub_train = training_data[:initial_size]
    sub_test = testing_data

    steps = 0
    rank_diffs = []
    while (initial_size+steps) < len(training_data) - 1:
        train_new_ds = []
        count = 0
        # Setting up training data
        for i, sub_train_a in enumerate(sub_train):
            for j, sub_train_b in enumerate(sub_train):
                if i==j: continue
                print ". ",
                temp = []
                temp.extend(sub_train_a.decisions)
                temp.extend(sub_train_b.decisions)
                assert(len(temp) == 2 * len(sub_train_a.decisions)), "Something is wrong"
                dep_value = domination(sub_train_a.objectives, sub_train_b.objectives, mins, maxs)
                train_new_ds.append(data_point(count, temp, dep_value))
                count += 1
        print
        # Setting up testing data
        test_new_ds = []
        count = 0
        for i, sub_test_a in enumerate(sub_test):
            for j, sub_test_b in enumerate(sub_test):
                if i==j: continue
                print ". ",
                temp = []
                temp.extend(sub_test_a.decisions)
                temp.extend(sub_test_b.decisions)
                assert(len(temp) == 2 * len(sub_test_b.decisions)), "Something is wrong"
                dep_value = domination(sub_test_a.objectives, sub_test_b.objectives, mins, maxs)
                test_new_ds.append(data_point(count, temp, dep_value))
                count += 1

        print
        print len(train_new_ds), len(training_data)
        print len(test_new_ds), len(testing_data)

        predicted_dependent = build_regressor(train_new_ds, test_new_ds)

        # predicted_domination
        test if the prediction model can predict for domination policy_result
        go through all the points and see if the domination can be predicted

        import pdb
        pdb.set_trace()


        rank_diffs.append(mean_rank_diff)
        policy_result = policy1(rank_diffs)
        if policy_result is True : break
        steps += 1
        sub_train.append(training_data[initial_size+steps])
    return sub_train

if __name__ == "__main__":
    from utility import read_file, split_data, build_model
    from non_dominated_sort import non_dominated_sort
    file = "./Data/noc_CM_log.csv"
    data = read_file(file)
    splits = split_data(data, 40, 5, 55)
    temp = rank_based_approach(splits[0], splits[1])

    predicted_dependent = build_model(temp, splits[2])

    actual_dependent = [d.objectives for d in splits[2]]

    true_pf_indexes = non_dominated_sort(actual_dependent)
    predicted_pf_indexes = non_dominated_sort(predicted_dependent)
    # Actual Dependent values of the predicted_pf
    predicted_actual =[actual_dependent[i] for i in predicted_pf_indexes]
    # As an additional filter and second round of non-dominated sorting is performed == No additional evaluations
    filtered_predicted_pf_index = non_dominated_sort(predicted_actual)

    true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])
    print
    # predicted_pf = sorted([predicted_actual[i] for i in filtered_predicted_pf_index], key=lambda x:x[0])
    predicted_pf = sorted([actual_dependent[i] for i in predicted_pf_indexes], key=lambda x:x[0])

    from utility import draw_pareto_front, generational_distance
    draw_pareto_front(actual_dependent, true_pf, predicted_pf) #, filename=file.split('/')[-1])
    print "Length of Training set: ", len(temp)
    print "Length of Validation set: ", len(splits[1])
    print "Generation Distance: ", generational_distance(true_pf, predicted_pf)


