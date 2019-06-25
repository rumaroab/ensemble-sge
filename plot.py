import json
import matplotlib.pyplot as plt



def readFile(name = "res.json"):
    return json.load(open(name))


def main():

    data = readFile("res.1.json")
    plt.plot([data[i]["result"] for i in range(len(data)) ])
    #plt.plot([data[i]["best"] for i in range(len(data)) ])
    plt.ylabel([data[i]["generation"] for i in range(len(data)) ])
    plt.show()

main()
    