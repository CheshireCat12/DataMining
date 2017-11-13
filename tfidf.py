import operator
from math import log


def initializeWordCount(documentNameIn):
    documentNameOut = "wordsOut.txt"

    linesIn = loadAllData(documentNameIn)
    linesOut = {}
    nbOccurenceWordInDocument = {}

    totalNumberOfDocument = linesIn[-1].split()[0]

    print("Creation of the dictionary...")
    for dataIn in linesIn:

        lineInWithoutId = dataWithoutId(dataIn)
        idListIn = lineInWithoutId[0]

        if idListIn in linesOut:
            linesOut[idListIn] += int(lineInWithoutId[1])
            nbOccurenceWordInDocument[idListIn] += 1
        else:
            linesOut[idListIn] = int(lineInWithoutId[1])
            nbOccurenceWordInDocument[idListIn] = 1

    idfDict = idf(nbOccurenceWordInDocument, totalNumberOfDocument)

    for idWord in linesOut:
        linesOut[idWord] = linesOut[idWord] * idfDict[idWord]

    linesOut = sortDictionaryByValue(linesOut)

    writeDataInFile(documentNameOut, linesOut)


def idf(nbOccurenceWordInDocument, numberOfDocument):
    for termId in nbOccurenceWordInDocument:
        nbOccurenceWordInDocument[termId] = log(
            int(numberOfDocument) / nbOccurenceWordInDocument[termId])
    return nbOccurenceWordInDocument


def sortDictionaryByValue(dictionary):
    print("Sorting dictionary...")
    sortedDictionary = sorted(
        dictionary.items(), key=operator.itemgetter(1), reverse=True)[:10]
    return [k + " " + str(v) + "\n" for k, v in sortedDictionary]


def loadAllData(pathFileName):
    print("Loading data...")
    dataLoaded = list()
    for i in range(1, 4):
        data = getListWordsFromFile(pathFileName.format(i))
        dataLoaded += data

    return dataLoaded


def getListWordsFromFile(fileName):
    with open(fileName) as fileIn:
        return fileIn.readlines()


def dataWithoutId(line):
    return line.split()[1:]


def writeDataInFile(fileName, data):
    print("Writing data..")
    with open(fileName, 'w+') as fileOut:
        fileOut.writelines(data)


def makeClusteringData(fileNameDocWords, fileNameWordsOut):
    docWords = loadAllData(fileNameDocWords)
    wordsOut = getListWordsFromFile(fileNameWordsOut)


if __name__ == "__main__":
    path = "nsfabs_part{0}_out/docwords.txt"
    initializeWordCount(path)
