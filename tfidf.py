import operator


def initializeWordCount(documentNameIn):
    documentNameOut = "wordsOut.txt"

    linesIn = loadAllData()
    linesOut = {}
    termNumDoc = {}

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

    print(len(linesOut))

    #isInList = False
    # for i in range(len(linesOut)):
    #     splitedLine = linesOut[i].split()

    #     idListOut = int(splitedLine[0])
    #     idListIn = int(lineInWithoutId[0])

    #     if idListIn == idListOut:
    #         linesOut[i] = computeNewFrequence(splitedLine, lineInWithoutId)
    #         isInList = True
    #         break
    #     elif idListIn < idListOut:
    #         linesOut.insert(i, " ".join(lineInWithoutId) + "\n")
    #         isInList = True
    #         break

    # if not isInList:
    #     linesOut.append(" ".join(lineInWithoutId) + "\n")
    #print(sorted(linesOut, key=getKey))
    # print(linesOut)
    #writeDataInFile(documentNameOut, linesOut)


def sortDictionaryByValue(dictionary):
    print("Sorting dictionary")
    return sorted(dictionary.items(), key=operator.itemgetter(1))


def getKey(item):
    return int(item.split()[0])


def loadAllData():
    print("Loading data...")
    dataLoaded = list()
    for i in range(1, 4):
        data = getListWordsFromFile(
            "nsfabs_part{0}_out/docwords.txt".format(i))
        dataLoaded += data

    print(len(dataLoaded))
    return dataLoaded


def getListWordsFromFile(fileName):
    with open(fileName) as fileIn:
        return fileIn.readlines()


def dataWithoutId(line):
    return line.split()[1:]


def computeNewFrequence(oldLine, newLine):
    return oldLine[0] + " " + str(int(oldLine[1]) + int(newLine[1])) + "\n"


def writeDataInFile(fileName, data):
    with open(fileName, 'w+') as fileOut:
        fileOut.writelines(data)


if __name__ == "__main__":
    path = "nsfabs_part1_out/docwordsMinim"
    initializeWordCount(path)
