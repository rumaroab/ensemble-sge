import json
from math import log, exp, sqrt
from numpy import median, mean
from statistics import mode
from math import sin, cos, tan
from dsge.core.grammar import Grammar
from dsge.core.protectedmath import _log_, _div_, _exp_, _inv_, _sqrt_, protdiv
import time

__invalid_fitness = 9999999
testset_path = 'datasets/housing.txt'
test_indexes = 'datasets/housing.folds'

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

    with open(test_indexes, 'r') as dataset_folds:
        for line in dataset_folds:
            folds = line.split()
            test_set = [dataset[int(i)] for i in folds]
            break
    return test_set

def run(ind, grammar, dataset):
    mapping_values = [0 for i in ind['genotype']]
    phen, tree_depth = grammar.mapping(ind['genotype'], mapping_values)
    quality, other_info = evaluate(phen,dataset)
    ind['quality'] = quality
    ind['other_info'] = other_info
    ind['mapping_values'] = mapping_values
    ind['tree_depth'] = tree_depth
    

def groupFunc(values, type = 0):
    if type == 1:
        return mean(values)
    elif type == 2:
        return mode(values)
    else:
        return median(values)

def evalEns(dataset,pop,grammar):
    __RRSE_test_denominator = calculate_RRSE_denominators(dataset)
    error = ensError(dataset,pop,grammar)
    test_error = _sqrt_( error / float(__RRSE_test_denominator))
    return test_error

def ensError(dataset,pop,grammar): 
    pred_error = 0
    for fit_case in dataset:
        case_output = fit_case[-1]
        results = []
        for individual in pop:
            mapping_values = [0 for i in individual['genotype']]
            phen, tree_depth = grammar.mapping(individual['genotype'], mapping_values)
            try:
                result = eval(phen, globals(), {"x": fit_case[:-1]})
                results.append(result)
            except (OverflowError, ValueError) as e:
                continue
        groupResult = groupFunc(results,1)
        pred_error += (case_output - groupResult)**2
    return pred_error

def perGeneration():
    newPop = []
    for i in range(51):
        if i == 0:
            continue
        tempGeneration = json.load(open("datasets/BostonHousing_pop1000/run_0/iteration_"+ str(i) +".json"))
        tempGeneration.sort(key=lambda x: x["fitness"])
        count = 0
        for individual in tempGeneration:
            if count == 20:
                break
            newPop.append(individual)
            count +=1

    return newPop


def getPop(type = 0, gen = 50):
    if type == 1:
        return perGeneration()
    else:
        return json.load(open("datasets/BostonHousing_pop1000/run_0/iteration_"+str(gen)+".json"))

def main():
    #read test dataset
    dataset = read_testset()
    print(len(dataset))
    
    #calc rsse
    rsse = calculate_RRSE_denominators(dataset)

    #get Grammar
    grammar = Grammar("dsge/grammars/boston_housing_grammar.txt", 6, 17)
    
    resultEvo = []
    for gen in range(50):
        # get Pop
        # type = 1 : 20 elements for each generation 
        population = getPop(gen = gen)
        # temp = []
        # for ind in population:
        #     run(ind,grammar,dataset)
        #     temp.append(ind)
        population.sort(reverse=False, key=lambda x: x["other_info"]["test_error"])
        
        #Evaluate Ensemble
        ensResult = evalEns(dataset,population,grammar)
        # best = min(temp)
        # worst = max(temp)

        print("\nINFO")
        print('ensemble: ' + str(ensResult) )
        # print('best: ' + str(min(temp)) )
        # print('worst: ' + str(max(temp)) )    
        # print('median: ' + str(median(temp)))   
        # resultEvo.append({ "generation": gen, "ensemble": ensResult, "best": best, "worst": worst})

    print(resultEvo)
    wr = json.dumps(resultEvo)
    open('results/%d.json' % (time.time()), 'w').write(wr)

main()