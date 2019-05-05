import json
from math import log, exp, sqrt
from numpy import median
from math import sin, cos, tan
from dsge.core.grammar import Grammar
from dsge.core.protectedmath import _log_, _div_, _exp_, _inv_, _sqrt_, protdiv

__invalid_fitness = 9999999
testset_path = 'datasets/housing_test.txt'

def calculate_RRSE_denominators(dataset):
    __RRSE_test_denominator = 0
    test_outputs = [entry[-1] for entry in dataset]
    test_output_mean = float(sum(test_outputs)) / len(test_outputs)
    __RRSE_test_denominator = sum([(i - test_output_mean)**2 for i in test_outputs])
    return __RRSE_test_denominator

def get_error(individual, dataset):
    pred_error = 0
    for fit_case in dataset: 
        case_output = fit_case[-1]
        try:
            result = eval(individual, globals(), {"x": fit_case[:-1]})
            pred_error += (case_output - result)**2
        except (OverflowError, ValueError) as e:
            return __invalid_fitness
    return pred_error

def evaluate(individual, dataset):
    __RRSE_test_denominator = calculate_RRSE_denominators(dataset)
    if individual == None:
        return None
    error = get_error(individual, dataset)
    test_error = _sqrt_( error / float(__RRSE_test_denominator))
    return (test_error,{'generation':0, "evals" : 1, "test_error" : test_error})

def read_testset():
    dataset = []
    with open(testset_path, 'r') as dataset_file:
        for line in dataset_file:
            dataset.append([float(value.strip(" ")) for value in line.split(" ") if value != ""])
    return dataset

def run(ind, grammar, dataset):
    mapping_values = [0 for i in ind['genotype']]
    phen, tree_depth = grammar.mapping(ind['genotype'], mapping_values)
    quality, other_info = evaluate(phen,dataset)
    ind['quality'] = quality
    ind['other_info'] = other_info
    ind['mapping_values'] = mapping_values
    ind['tree_depth'] = tree_depth
    
def main():
    #read test dataset
    dataset = read_testset()
    #calc rsse
    rsse = calculate_RRSE_denominators(dataset)
    #get Grammar
    grammar = Grammar("dsge/grammars/boston_housing_grammar.txt", 6, 17)
    
    #get Pop
    population = json.load(open("datasets/BostonHousing/run_0/iteration_1.json"))
    #population = json.load(open("datasets/BostonHousing_2/run_0/iteration_50.json"))
    
    

    temp = []
    for ind in population:
        run(ind,grammar,dataset)
        print(ind['quality'])
        temp.append(ind['quality'])

    print('median: ' + str(median(temp)))
    print('best: ' + str(min(temp)))
    print('worst: ' + str(max(temp)))
    
main()