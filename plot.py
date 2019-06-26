import json
import matplotlib.pyplot as plt



def readFile(name = "res.json"):
    return json.load(open(name))


def main():
    data = readFile("results/pagie/run_5_1561508586.json")
    #data = readFile("results/boston/1561493217.json")
    plt.plot([data[i]["ensemble"] for i in range(len(data))])
    plt.plot([data[i]["best"]for i in range(len(data))])
    plt.ylabel([data[i]["generation"] for i in range(len(data)) ])
    plt.show()

main()
    