from __future__ import division
import pandas as pd
import os, sys
import numpy as np


# Class for data_point
class data_point:
    def __init__(self, id, decisions, objectives, rank=None):
        self.id = id
        self.decisions = decisions
        self.objectives = objectives
        self.rank = rank
        self.evaluated = False

    def set_rank(self, rank):
        self.rank = rank

    def set_evaluated(self):
        self.evaluated = True

    def __str__(self):
        return "Id: " + str(self.id) + " Independent Values: " + ','.join(map(str, self.decisions)) +\
               " Dependent Values: " + ','.join(map(str, self.objectives))


class container(object):
    def __init__(self, name, epsilon_value):
        self.name = name
        self.epsilon_value = epsilon_value
        # Pareto Front Size
        self.pfs = []
        self.evals = []

    def set_evals(self, evals):
        self.evals = evals

    def append_eval(self, eval):
        self.evals.append(eval)

    def append_pfs(self, pfs):
        self.pfs.append(pfs)

    def set_pfs(self, pfs):
        self.pfs = pfs

# Read from a file and return a dataframe
def read_file(filename):
    content = pd.read_csv(filename)
    columns = content.columns
    independent_values = content[[c for c in columns if '<$' not in c]].values.tolist()
    dependent_values = content[[c for c in columns if '<$' in c]].values.tolist()
    data = []
    for i,(indep, dep) in enumerate(zip(independent_values, dependent_values)):
        data.append(data_point(i, indep, dep))
    return data


# Split data into training, testing and validation
def split_data(data, training_percent, testing_percent, validation_percent):
    assert(training_percent + testing_percent + validation_percent == 100), "Something is wrong"
    # For easy access
    dict_store = {}
    for d in data: dict_store[d.id] = d
    indexes = [i for i in xrange(len(data))]

    from random import shuffle
    shuffle(indexes)
    shuffled_data = [dict_store[i] for i in indexes]

    cut1 = int(len(data) * (training_percent)/100)
    cut2 = int(len(data) * (testing_percent/100)) + cut1

    assert(len(shuffled_data[:cut1]) + len(shuffled_data[cut1:cut1+cut2]) + len(shuffled_data[cut1+cut2:]) == len(data)), "Something is wrong"
    return [shuffled_data[:cut1], shuffled_data[cut1:cut2], shuffled_data[cut1+cut2:]]


def build_model(training, testing):
    training_independent = [t.decisions for t in training]
    training_dependent = [t.objectives for t in training]

    testing_independent = [t.decisions for t in testing]
    testing_dependent = [t.objectives for t in testing]

    predictions = []
    no_of_objectives = len(training_dependent[0])
    from sklearn.tree import DecisionTreeRegressor
    for objective_no in xrange(no_of_objectives):
        train_dependent_value = [t[objective_no] for t in training_dependent]
        model = DecisionTreeRegressor()
        model.fit(training_independent, train_dependent_value)
        predicted = model.predict(testing_independent)
        predictions.append(predicted)

    # change shape
    return_predictions = []
    for i in xrange(len(predictions[0])):
        return_predictions.append([predictions[obj_no][i] for obj_no in xrange(no_of_objectives)])
    assert(len(return_predictions) == len(predictions[0])), "Something is wrong"
    assert(len(return_predictions[0]) == no_of_objectives), "Something is wrong"
    return return_predictions


def draw_pareto_front(actual_dependent, true_pf, predicted_pf, filename=""):
    import matplotlib.pyplot as plt
    plt.scatter([d[0] for d in actual_dependent], [d[1] for d in actual_dependent], color='r')
    plt.plot([p[0] for p in true_pf], [p[1] for p in true_pf], color='black', marker='x', markersize=15)
    plt.plot([p[0] for p in predicted_pf], [p[1] for p in predicted_pf], color='green', marker='o')
    if filename == "": plt.show()
    else: plt.savefig('./AL3_Figures/' + filename + ".png")
    plt.cla()


def generational_distance(actual, predicted, ranges):
    def euclidean_distance(rlist1, rlist2):
        list1 = [(element - ranges[obj_no][0])/(ranges[obj_no][1] - ranges[obj_no][0]) for obj_no, element in enumerate(rlist1)]
        list2 = [(element - ranges[obj_no][0])/(ranges[obj_no][1] - ranges[obj_no][0]) for obj_no, element in enumerate(rlist2)]
        assert(len(list1) == len(list2)), "The points don't have the same dimension"
        distance = sum([(i - j) ** 2 for i, j in zip(list1, list2)])
        assert(distance >= 0), "Distance can't be less than 0"
        return distance

    min_distances = []
    for a in actual:
        min_dist = sys.maxint
        for p in predicted:
            min_dist = min(min_dist, euclidean_distance(a, p))
        min_distances.append(min_dist)
    return np.mean(min_distances)

ranges = {}
# ranges[filename] = [[min(obj1), max(obj2)], [min(obj2), max(obj2)]]
ranges["./Data/wc+sol-3d-c4.csv"] =  [[3983.3, 63734.0], [2.1844, 93904.0]]
ranges["./Data/wc-c3-3d-c1.csv"] =  [[121.5, 11930.0], [247.45, 57645.0]]
ranges["./Data/noc_CM_log.csv"] =  [[6.144515496, 9.965784285], [4.309193816, 5.123159887]]
ranges["./Data/wc-c1-3d-c1.csv"] =  [[288.56, 23075.0], [148.88, 9421.0]]
ranges["./Data/llvm_input.csv"] =  [[199.68, 270.4], [11.0, 29.0]]
ranges["./Data/sort_256.csv"] =  [[7.087462841, 16.24881706], [2.858160813, 14.71664238]]
ranges["./Data/wc-6d-c1.csv"] =  [[72.75, 34740.0], [3.3172, 55209.0]]
ranges["./Data/wc+rs-3d-c4.csv"] =  [[4275.4, 72394.0], [1.9243, 99722.0]]
ranges["./Data/wc-3d-c4.csv"] =  [[5042.6, 95094.0], [1.2994, 94553.0]]
ranges["./Data/wc-5d-c5.csv"] =  [[2122.2, 20591.0], [47.387, 405.5]]
ranges["./Data/rs-6d-c3.csv"] =  [[68.062, 232000.0], [1.9, 34733.0]]
ranges["./Data/wc+wc-3d-c4.csv"] =  [[3964.2, 65823.0], [2.0815, 105000.0]]


lessismore = {}
lessismore['./Data/llvm_input.csv'] = [False, False]
lessismore['./Data/noc_CM_log.csv'] = [False, False]
lessismore['./Data/sort_256.csv'] = [False, False]
lessismore['./Data/rs-6d-c3.csv'] = [False, True]
lessismore['./Data/wc+rs-3d-c4.csv'] = [False, True]
lessismore['./Data/wc+sol-3d-c4.csv'] = [False, True]
lessismore['./Data/wc+wc-3d-c4.csv'] = [False, True]
lessismore['./Data/wc-3d-c4.csv'] = [False, True]
lessismore['./Data/wc-5d-c5.csv'] = [False, True]
lessismore['./Data/wc-6d-c1.csv'] = [False, True]
lessismore['./Data/wc-c1-3d-c1.csv'] = [False, True]
lessismore['./Data/wc-c3-3d-c1.csv'] = [False, True]

if __name__ == "__main__":
    files = ["./Data/" + file for file in os.listdir('./Data/') if ".csv" in file]
    for file in files:
        data = read_file(file)
        split_data(data, 40, 20, 40)

