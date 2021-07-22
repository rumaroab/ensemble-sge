import json
from math import log, exp, sqrt
from numpy import median, mean
from numpy import percentile
from math import sin, cos, tan
from dsge.src.core.grammar import Grammar
from dsge.src.core.protectedmath import _log_, _div_, _exp_, _inv_, _sqrt_, protdiv
from scipy.stats import iqr
import math
import time
import matplotlib.pyplot as plt
RUN = "run_5"

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

def evalEns(dataset,pop,grammar,aggfn):
    __RRSE_test_denominator = calculate_RRSE_denominators(dataset)
    error = ensError(dataset,pop,grammar,aggfn)
    test_error = _sqrt_( error / float(__RRSE_test_denominator))
    return test_error

def groupFunc(values, type = 0):
    if type == 1:
        return mean(values)
    elif type == 2:
        return mode(values)
    else:
        return median(values)

def ensError(dataset,pop,grammar,aggfn): 
    pred_error = 0
    for fit_case in dataset:
        case_output = fit_case[-1]
        results = []
        for individual in pop:
            # mapping_values = [0 for i in individual['genotype']]
            # phen, tree_depth = grammar.mapping(individual['genotype'], mapping_values)
            phen = individual['phenotype']
            try:
                result = eval(phen, globals(), {"x": fit_case[:-1]})
                results.append(result)
            except (OverflowError, ValueError) as e:
                continue
        groupResult = groupFunc(results, aggfn)
        pred_error += (case_output - groupResult)**2
    return pred_error

def perGeneration(grammar, dataset):
    newPop = []
    for i in range(51):
        if i == 0:
            continue
        tempGeneration = json.load(open("datasets/Pagie/"+RUN+"/iteration_"+ str(i) +".json"))
        for ind in tempGeneration:
            run(ind, grammar, dataset)
        tempGeneration.sort(reverse=False,key=lambda x: x["other_info"]["test_error"] )
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
    return pop[:10]

def uniqueHundred(pop):
    pop.sort(reverse=False, key=lambda x: x["other_info"]["test_error"])
    seen = []
    for ind in pop:
        if ind in seen:
            continue
        seen.append(ind)
        yield ind
        if len(seen) == 500:
            return

def onlyIQR(pop):
    q3, q1 = percentile([ind["other_info"]["test_error"] for ind in pop], [75 ,25])
    temp = []
    for ind in pop:
        if ind["other_info"]["test_error"] >= q1 and ind["other_info"]["test_error"] <= q3 :
            temp.append(ind)
    return temp

def getPop(dataset, grammar, type = 0, gen = 50, folder = "pagie"):
    if type == 4:
        return perGeneration(grammar, dataset)
    
    pop = json.load(open("dumps/Regression/"+str(folder)+"/iteration_"+str(gen)+".json"))
    #fill test_error
    for ind in pop:
        run(ind, grammar, dataset)
        if math.isnan(ind["other_info"]["test_error"]):
            return []

    if type == 0:
        return pop
    if type == 1:
        return list(uniqueHundred(pop))
    if type == 2:
        return hundredBest(pop)
    if type == 3:
        return onlyIQR(pop)
    
def analyse():
    grammar = Grammar("dsge/src/grammars/regression.txt")
    xx = list(drange(-5,5.0,.1))
    yy = list(drange(-5,5.0,.1))
    func = eval("quarticpolynomial")
    zz = map(func, xx, yy)
    dataset = zip(xx,yy,zz)
    
    pop = json.load(open("dumps/Regression/pagie/iteration_50.json"))
    #fill test_error
    teData = []
    qData = []
    data = []
    for ind in pop:
        run(ind, grammar, dataset)
        teData.append(ind["other_info"]["test_error"])
        qData.append(ind["quality"])
        data.append((ind["quality"],ind["other_info"]["test_error"]))
     
    fig1, ax1 = plt.subplots()
    ax1.set_title('testError')
    ax1.boxplot(teData, showfliers=False)

    fig7, ax7 = plt.subplots()
    ax7.set_title('qlty')
    ax7.boxplot(qData, showfliers=False)
    
    plt.show()

    
           

def main(function = "pagiepolynomial"):
    typs = [2]
    aggFns = [0,1] 
    for typ in typs:
        for aggFn in aggFns:
            gen = 50
            grammar = Grammar("dsge/src/grammars/regression.txt")
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
            for gen in range(50):
                # type = 0 : full pop
                # type = 1 : best 100 unique ind in pop 
                # type = 2 : best 100 ind in pop 
                # type = 3 : only in IQR
                # type = 4 : 20 elements per generation
                #typ = 0
                # type = 0 : median
                # type = 1 : mean 
                # type = 2 : mode 
                #aggFn = 1
                # fn = paigie
                # fn = quartic
                fn="pagie"

                population = getPop(grammar=grammar, dataset=dataset, type=typ, gen = gen, folder=fn)
                size = len(population)
                if size == 0:
                    print("NaN")
                    resultEvo.append({ "generation": gen, "ensemble": 0, "best": 0, "worst": 0})
                    continue
                print(size)
                
                #wrpop = json.dumps(population)
                #open('results/pagie_pop_per20.json', 'w').write(wrpop)
                
                #Evaluate Ensemble
                ensResult = evalEns(dataset,population,grammar,aggFn)
                temp = [ind["other_info"]["test_error"] for ind in population]
                tempf = [ind["fitness"] for ind in population]
                try: 
                    bestf = min(tempf)
                except: 
                    bestf = -1

                try: 
                    worstf = min(temp)
                except: 
                    worstf = -1

                try: 
                    best = min(temp)
                except: 
                    best = -1
                try: 
                    worst = max(temp)
                except: 
                    worst = -1

                print("\nINFO: "+ str(gen))
                print('ensemble: ' + str(ensResult) ) 
                print('best: ' + str(best))
                print('worst: ' + str(worst))
                # print('median: ' + str(median(temp)))   
                resultEvo.append({ "generation": gen, "ensemble": ensResult, "best": best, "worst": worst, "bestf": bestf, "worstf": worstf})

            print(resultEvo)
            wr = json.dumps(resultEvo)
            open('results/v2/symbolic_'+str(fn)+'_poli_'+str(typ)+'_'+str(aggFn)+'_10_fitness.json', 'w').write(wr)
main()