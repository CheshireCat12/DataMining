import operator


def initializeWordCount(documentNameIn):
    documentNameOut = "wordsOut.txt"

    linesIn = loadAllData()
    linesOut = {}

    nbDocument = linesIn[-1].split()[0]
    print(nbDocument)

    print("Creation of the dictionary...")
    for dataIn in linesIn:

        lineInWithoutId = dataWithoutId(dataIn)
        idListIn = lineInWithoutId[0]

        if idListIn in linesOut:
            linesOut[idListIn] += int(lineInWithoutId[1])
        else:
            linesOut[idListIn] = int(lineInWithoutId[1])


def sortDictionaryByValue(dictionary):
    print("Sorting dictionary")
    return sorted(dictionary.items(), key=operator.itemgetter(1))


def loadAllData():
    print("Loading data...")
    dataLoaded = list()
    for i in range(1, 4):
        data = getListWordsFromFile(
            "nsfabs_part{0}_out/docwords.txt".format(i))
        dataLoaded += data

    return dataLoaded


def getListWordsFromFile(fileName):
    with open(fileName) as fileIn:
        return fileIn.readlines()


def dataWithoutId(line):
    return line.split()[1:]


def writeDataInFile(fileName, data):
    with open(fileName, 'w+') as fileOut:
        fileOut.writelines(data)


if __name__ == "__main__":
    path = "nsfabs_part1_out/docwordsMinim"
    initializeWordCount(path)
