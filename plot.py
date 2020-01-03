import json
import matplotlib.pyplot as plt



def readFile(name = "res.json"):
    return json.load(open(name))


def main():
    # data = readFile("results/relevant/pagie_run_5_100.json")
    # data1 = readFile("results/relevant/pagie_run_5_100unique.json")
    # data2 = readFile("results/relevant/pagie_run_5_100unique_mean.json")
    # data3 = readFile("results/relevant/pagie_run_5_100_mean.json")
    # data4 = readFile("results/relevant/pagie_run_5_full.json")
    #data = readFile("results/relevant/pagie_run_5_1iqr3_mean.json")
    #data = readFile("results/boston/1561493217.json")
    title = "Boston 100 "
    grname = "boston_100_1"
    filename = "boston_run_0_100_mean"
    filename1 = "boston_run_0_100"
    data = readFile("results/relevant/"+filename+".json")
    data1 = readFile("results/relevant/"+filename1+".json")
    # plt.subplot(131)
    # plt.plot([data[i]["ensemble"] for i in range(len(data))], color="red")
    # plt.plot([data[i]["best"]for i in range(len(data))], color="green")
    # plt.ylabel([data[i]["generation"] for i in range(len(data)) ])
    # plt.subplot(132)
    # plt.plot([data1[i]["ensemble"]for i in range(len(data1))], color="blue")
    # plt.plot([data1[i]["best"]for i in range(len(data1))], color="green")
    # plt.ylabel([data1[i]["generation"] for i in range(len(data1)) ])
    # plt.subplot(133)
    # plt.plot([data2[i]["ensemble"]for i in range(len(data2))], color="orange")
    # plt.plot([data2[i]["best"]for i in range(len(data2))], color="green")
    # plt.ylabel([data2[i]["generation"] for i in range(len(data2)) ])
    # plt.subplot(133)
    # plt.plot([data4[i]["ensemble"]for i in range(len(data4))], color="pink")
    # plt.plot([data4[i]["best"]for i in range(len(data4))], color="green")
    # plt.ylabel([data4[i]["generation"] for i in range(len(data4)) ])
    # plt.subplot(131)
    # plt.plot([data3[i]["ensemble"]for i in range(len(data3))], color="yellow")
    # plt.plot([data3[i]["best"]for i in range(len(data3))], color="green")
    # plt.ylabel([data3[i]["generation"] for i in range(len(data3)) ])
    # plt.show()
    plt.title(title)
    plt.plot([data[i]["ensemble"]for i in range(len(data))], color="red", label='Ensemble Mean')
    plt.plot([data1[i]["ensemble"]for i in range(len(data))], color="orange", label='Ensemble Median')
    plt.plot([data[i]["best"]for i in range(len(data))], color="green", label='SGE')
    plt.legend()
    plt.ylabel([data[i]["generation"] for i in range(len(data)) ])    
    plt.savefig('results/plots/'+grname+'.png')
    plt.show()
main()
    