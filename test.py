

import json

for i in range(50):
    individuals = json.load(open("dumps/Regression/pagie/iteration_20.json"))
    #temp = [ind["other_info"]["test_error"] for ind in individuals]
    #print(min(temp), max(temp))
    temp = [ind["fitness"] for ind in individuals]
    print(i, min(temp), max(temp))
    # individuals.sort(reverse=False, key=lambda x: x["fitness"])
    # i = 0
    # for individual in individuals:
    #     print(individual["other_info"]["test_error"])
    #     print(individual["fitness"])
    #     if i == 10:
    #         break
    #     i += 1