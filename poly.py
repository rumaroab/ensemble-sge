import json
from math import log, exp, sqrt
from numpy import median, mean
from numpy import percentile
from statistics import mode
from math import sin, cos, tan
from dsge.core.grammar import Grammar
from dsge.core.protectedmath import _log_, _div_, _exp_, _inv_, _sqrt_, protdiv
from scipy.stats import iqr

import time
__invalid_fitness = 9999999
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step
def calculate_RRSE_denominators(dataset):
    __RRSE_test_denominator = 0
    test_outputs = [entry[-1] for entry in dataset]
    test_output_mean = float(sum(test_outputs)) / len(test_outputs)
    __RRSE_test_denominator = sum([(i - test_output_mean)**2 for i in test_outputs])
    return __RRSE_test_denominator
def run(ind, grammar, dataset):
    mapping_values = [0 for i in ind['genotype']]
    phen, tree_depth = grammar.mapping(ind['genotype'], mapping_values)
    quality, other_info = evaluate(phen,dataset)
    ind['quality'] = quality
    ind['other_info'] = other_info
    ind['mapping_values'] = mapping_values
    ind['tree_depth'] = tree_depth
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
    error = 0.0
    if individual == None:
        return None
    error = get_error(individual, dataset)
    error = _sqrt_( error /__RRSE_test_denominator)
    if error == None:
        error = __invalid_fitness
    return (error,{'generation':0, "evals" : 1, "test_error" : error})

def evalEns(dataset,pop,grammar):
    __RRSE_test_denominator = calculate_RRSE_denominators(dataset)
    error = ensError(dataset,pop,grammar)
    test_error = _sqrt_( error / float(__RRSE_test_denominator))
    return test_error

def groupFunc(values, type = 0):
    if type == 1:
        return mean(values)
    elif type == 2:
        return mode(values)
    else:
        return median(values)

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
        groupResult = groupFunc(results)
        pred_error += (case_output - groupResult)**2
    return pred_error

def perGeneration():
    newPop = []
    for i in range(51):
        if i == 0:
            continue
        tempGeneration = json.load(open("datasets/Pagie/run_0/iteration_"+ str(i) +".json"))
        tempGeneration.sort(key=lambda x: x["fitness"])
        count = 0
        for individual in tempGeneration:
            if count == 20:
                break
            newPop.append(individual)
            count +=1

    return newPop

def quarticpolynomial(inp):
    return pow(inp,4) + pow(inp,3) + pow(inp,2) + inp

def pagiepolynomial(inp1,inp2):
    return 1.0 / (1 + pow(inp1,-4.0)) + 1.0 / (1 + pow(inp2,-4))

def hundredBest(pop):
    pop.sort(reverse=False, key=lambda x: x["other_info"]["test_error"])
    return pop[:100]

def uniqueHundred(pop):
    pop.sort(reverse=False, key=lambda x: x["other_info"]["test_error"])
    seen = []
    for ind in pop:
        if ind in seen:
            continue
        seen.append(ind)
        yield ind
        if len(seen) == 100:
            return

def onlyIQR(pop):
    q3, q1 = percentile([ind["other_info"]["test_error"] for ind in pop], [75 ,25])
    temp = []
    for ind in pop:
        if ind["other_info"]["test_error"] >= q1 and ind["other_info"]["test_error"] <= q3 :
            temp.append(ind)
    return temp

def getPop(dataset, grammar, type = 0, gen = 50, folder = "Pagie"):
    pop = json.load(open("datasets/"+folder+"/run_2/iteration_"+str(gen)+".json"))
    #fill test_error
    for ind in pop:
        run(ind, grammar, dataset)

    if type == 0:
        return pop
    if type == 1:
        return list(uniqueHundred(pop))
    if type == 2:
        return hundredBest(pop)
    if type == 3:
        return onlyIQR(pop)
    if type == 4:
        return perGeneration()

def main(function = "pagiepolynomial"):
    gen = 50
    grammar = Grammar("dsge/grammars/regression.txt")
    if function == "pagiepolynomial":
        xx = list(drange(-5,5.0,.1))
        yy = list(drange(-5,5.0,.1))
        func = eval(function)
        zz = map(func, xx, yy)
        dataset = zip(xx,yy,zz)
    else:
        if function == "keijzer6":
            xx = list(drange(1,51,1))
        else:
            xx = list(drange(-1,1.1,.1))
        func = eval(function)
        yy = map(func,xx)
        dataset = zip(xx,yy)

    resultEvo = []
    for gen in range(51):
        # type = 0 : full pop
        # type = 1 : best 100 unique ind in pop 
        # type = 2 : best 100 ind in pop 
        # type = 3 : only in IQR
        # type = 4 : 20 elements per generation
        population = getPop(grammar=grammar, dataset=dataset, type=1, gen = gen)
        print(len(population))

        #Evaluate Ensemble
        ensResult = evalEns(dataset,population,grammar)
        temp = [ind["other_info"]["test_error"] for ind in population]

        best = min(temp)
        worst = max(temp)
        print("\nINFO: "+ str(gen))
        print('ensemble: ' + str(ensResult) ) 
        print('best: ' + str(best))
        print('worst: ' + str(worst))
        # print('median: ' + str(median(temp)))   
        resultEvo.append({ "generation": gen, "ensemble": ensResult, "best": best, "worst": worst})

    print(resultEvo)
    wr = json.dumps(resultEvo)
    open('results/pagie/%d.json' % (time.time()), 'w').write(wr)
main()