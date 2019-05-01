
import re, copy, itertools
import pdb
import random
import os
from pathlib import Path

original_dataset_path = '../datasets/housing.txt'
testset_path = '../datasets/housing_test.txt'
dataset_path = '../dsge/src/resources/housing.txt'
folds_path = '../dsge/src/resources/housing.folds'

class Ensemble():
    def __init__(self):
        self.__train_set = []
        self.__test_set = []
        self.__invalid_fitness = 9999999
        self.__run = 1
        self.read_dataset()
        self.test_set_size = len(self.__test_set)

    def read_dataset(self):
        dataset = []
        training_indexes = []
        test_indexes = []
        with open(original_dataset_path, 'r') as dataset_file:
            for line in dataset_file:
                dataset.append([float(value.strip(" ")) for value in line.split(" ") if value != ""])
        with open(folds_path, 'r') as folds_file:
            for i in range(self.__run - 1): folds_file.readline()
            test_indexes = folds_file.readline()
            test_indexes = [int(value.strip(" ")) - 1 for value in test_indexes.split(" ") if value != ""]
            training_indexes = filter(lambda x: x not in test_indexes, range(len(dataset))) #Not the most efficient way
        self.__train_set = [dataset[i] for i in training_indexes]
        self.__test_set = [dataset[i] for i in test_indexes]
        self.write_new_dataset(self.__train_set, self.__test_set)
    
    def write_new_dataset(self, training_set, test_set):
        if os.path.isfile(dataset_path) : 
            os.remove(dataset_path)
        Path(dataset_path).touch()
        if os.path.isfile(testset_path) : 
            os.remove(testset_path)
        Path(testset_path).touch()
        with open(dataset_path, 'a') as file:
            for row in training_set:
                file.write(' '.join(str(el) for el in row) + '\n')
        with open(testset_path, 'a') as tfile:
            for row in test_set:
                tfile.write(' '.join(str(el) for el in row) + '\n')
    
    def run(self):
        experience_name = "BostonHousing/"
        grammar = grammar.Grammar("../dsge/src/boston_housing_grammar.txt", 6, 17)
        evaluation_function = BostonHousing(1) 
        core.sge.evolutionary_algorithm(grammar = grammar, eval_func=evaluation_function, exp_name=experience_name)
        return True
        

    def evaluate(self):
        return True

    
        
ens = Ensemble()