import random

testset_path = 'datasets/housing.txt'

def createFolds(dataset, no = 50):
    allFolds = []
    data = ""
    for j in range(no):
        tempInt = random.randint(0,len(dataset))
        while tempInt in allFolds: 
            tempInt = random.randint(0,len(dataset))
        data += "%d " % tempInt
        allFolds.append(tempInt)
    
    return allFolds, data

def read_dataset():
    dataset = []
    with open(testset_path, 'r') as dataset_file:
        for line in dataset_file:
            dataset.append([float(value.strip(" ")) for value in line.split(" ") if value != ""])
    return dataset

def preprocessDatasets():
    dataset = read_dataset()
    #generate folds for validating ensemble
    ensembleFolds, strEnsembleFolds = createFolds(dataset)
    print("ENSEMBLE SETUP")
    print(len(dataset))
    print(ensembleFolds)

    #create new dataset without test examples
    newDataset = []
    for i,el in enumerate(dataset):
        if i not in ensembleFolds:
            newDataset.append(el)
    
    #generate folds with new dataset for sge
    sgeFolds, strSgeFolds = createFolds(newDataset)
    print("SGE SETUP")
    print(len(newDataset))
    print(sgeFolds)

    
preprocessDatasets()