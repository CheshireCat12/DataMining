from math import log
from copy import deepcopy
import operator


class Tfidf:

    def __init__(self, document, numberOfWordChosen):
        print("Creation of the class...")
        self.numberOfWordPerDocument = {}
        self.frequencePerWordInDocument = {}
        self.nbOccurenceWordInDocument = {}
        self.document = document
        self.numberOfWordChosen = numberOfWordChosen

    def getNumberOfWordInEachDocument(self):
        for lines in self.document:
            splittedLine = lines.split()
            idDoc = splittedLine[0]
            idWord = splittedLine[1]
            frequenceWord = int(splittedLine[2])

            self.getEachWordInDocument(idDoc, idWord, frequenceWord)
            self.getNumberOfOccurence(
                idDoc, frequenceWord, self.numberOfWordPerDocument)

    def getEachWordInDocument(self, idDoc, idWord, frequenceWord):
        if idDoc in self.frequencePerWordInDocument:
            self.frequencePerWordInDocument[idDoc][idWord] = frequenceWord
        else:
            self.frequencePerWordInDocument[idDoc] = {idWord: frequenceWord}

    def getNumberOfDocument(self):
        return int(self.document[-1].split()[0])

    def tf(self):
        copyOfFreqWord = deepcopy(self.frequencePerWordInDocument)

        for doc in self.frequencePerWordInDocument:
            for word in self.frequencePerWordInDocument[doc]:

                copyOfFreqWord[doc][word] /= self.numberOfWordPerDocument[doc]

                self.getNumberOfOccurence(
                    word,
                    1,
                    self.nbOccurenceWordInDocument)

        return copyOfFreqWord

    def getNumberOfOccurence(self, id, frequence, dictionary):
        dictionary[id] = dictionary.get(id, 0) + frequence

    def idf(self):
        numberOfDocument = self.getNumberOfDocument()
        copyOfOccurenceWord = deepcopy(self.nbOccurenceWordInDocument)

        print(numberOfDocument)

        for termId in copyOfOccurenceWord:
            copyOfOccurenceWord[termId] = log(
                numberOfDocument / copyOfOccurenceWord[termId])

        return copyOfOccurenceWord

    def tfidf(self, tfDict, idfDict):
        tfidfPerWords = {}

        for doc in tfDict:
            for words in tfDict[doc]:
                self.getNumberOfOccurence(
                    words, tfDict[doc][words], tfidfPerWords)

        for words in tfidfPerWords:
            tfidfPerWords[words] *= idfDict[words]

        return tfidfPerWords

    def sortAndSelectByValue(self, dictionary):
        print("Sorting dictionary...")

        sortedDictionary = sorted(
            dictionary.items(), key=operator.itemgetter(1), reverse=True)

        return sortedDictionary[:self.numberOfWordChosen]

    def writeResult(self, selectedWord, fileNameOut):
        result = {}

        for lines in self.frequencePerWordInDocument:
            result[lines] = list()
            for selected in selectedWord:
                temp = 0
                for word in self.frequencePerWordInDocument[lines]:
                    if word == selected[0]:
                        temp = selected[1]
                result[lines].append(temp)
        self.writeResultWords(selectedWord, fileNameOut)
        print("result ", result)
        with open(fileNameOut + "Array.txt", 'w+') as fileOut:
            for lines in result:
                fileOut.writelines(str(result[lines]) + "\n")

    def writeResultWords(self, selectedWord, fileNameOut):
        arrayOut = [k + " " + str(v) + "\n" for k, v in selectedWord]
        with open(fileNameOut + "Words.txt", "w+") as fileOut:
            fileOut.writelines(arrayOut)


def numberOfWordPerDocument(document):
    numOfWordInDocument = {}
    frequencePerWordInDocument = {}

    for lines in document:
        splittedLine = lines.split()
        idDoc = splittedLine[0]
        idWord = splittedLine[1]
        frequenceWord = int(splittedLine[2])

        if idDoc in frequencePerWordInDocument:
            frequencePerWordInDocument[idDoc][idWord] = frequenceWord
        else:
            frequencePerWordInDocument[idDoc] = {idWord: frequenceWord}

        if idDoc in numOfWordInDocument:
            numOfWordInDocument[idDoc] += frequenceWord
        else:
            numOfWordInDocument[idDoc] = frequenceWord

    totalNumberOfDocument = getNumberOfDocument(document)

    tfPerWords, nbOccurenceWordInDocument = tfOfWordPerDocument(
        numOfWordInDocument, frequencePerWordInDocument)
    # print(frequencePerWordInDocument)
    # print(numOfWordInDocument)
    #print( nbOccurenceWordInDocument)
    # print(tfPerWords)

    idfDict = idf(nbOccurenceWordInDocument, totalNumberOfDocument)
    # print(idfDict)

    tfIdfDict = tfidf(tfPerWords, idfDict)
    # print(tfIdfDict)

    sortedDict = sortDictionaryByValue(tfIdfDict)

    # print(frequencePerWordInDocument)

    print("sortedDict ", sortedDict)

    writableData(frequencePerWordInDocument, sortedDict)

    # return (numOfWordInDocument, frequencePerWordInDocument)


def writableData(document, selectedWord):
    result = {}
    for lines in document:
        result[lines] = list()
        for selected in selectedWord:
            temp = 0
            for word in document[lines]:
                # print(word)
                # print("selected", selected)
                if word == selected[0]:
                    temp = selected[1]
            result[lines].append(temp)
    print("result ", result)
    with open("result.txt", 'w+') as fileOut:
        for lines in result:
            fileOut.writelines(str(result[lines]) + "\n")


def sortDictionaryByValue(dictionary):
    print("Sorting dictionary...")
    sortedDictionary = sorted(
        dictionary.items(), key=operator.itemgetter(1), reverse=True)[:5]
    # [k + " " + str(v) + "\n" for k, v in sortedDictionary]
    return sortedDictionary


def tfidf(tfDict, idfDict):
    tfidfPerWords = {}
    # print(tfDict)
    for doc in tfDict:
        for words in tfDict[doc]:
            if words in tfidfPerWords:
                tfidfPerWords[words] += tfDict[doc][words]
            else:
                tfidfPerWords[words] = tfDict[doc][words]
    for words in tfidfPerWords:
        tfidfPerWords[words] *= idfDict[words]

    return tfidfPerWords


def idf(nbOccurenceWordInDocument, numberOfDocument):
    for termId in nbOccurenceWordInDocument:
        nbOccurenceWordInDocument[termId] = log(
            numberOfDocument / nbOccurenceWordInDocument[termId])
    return nbOccurenceWordInDocument


def tfOfWordPerDocument(numWordInDoc, freqWordPerDoc):
    copyToReturnOfFreqWord = deepcopy(freqWordPerDoc)
    nbOccurenceWordInDocument = {}

    for doc in freqWordPerDoc:
        for word in freqWordPerDoc[doc]:
            copyToReturnOfFreqWord[doc][word] /= numWordInDoc[doc]

            if freqWordPerDoc[doc][word] in nbOccurenceWordInDocument:
                nbOccurenceWordInDocument[word] += 1
            else:
                nbOccurenceWordInDocument[word] = 1

    return (copyToReturnOfFreqWord, nbOccurenceWordInDocument)


def getNumberOfDocument(document):
    return int(document[-1].split()[0])


def loadAllData(fileName):
    print("Loading data...")
    dataLoaded = list()
    for i in range(1, 4):
        data = getListWordsFromFile(fileName.format(i))
        dataLoaded += data

    return dataLoaded


def getListWordsFromFile(fileName):
    with open(fileName) as fileIn:
        return fileIn.readlines()


if __name__ == "__main__":
    fileName = "nsfabs_part{0}_out/docwords.txt"
    fileNameOut = "docWordsOut.txt"
    docWords = loadAllData(fileName)

    numberOfWordPerDocument(docWords[:100])

    myTfidf = Tfidf(docWords[:100], 5)
    myTfidf.getNumberOfWordInEachDocument()

    # print(myTfidf.numberOfWordPerDocument)
    # print(myTfidf.frequencePerWordInDocument)

    myTf = myTfidf.tf()
    # print(myTfidf.nbOccurenceWordInDocument)
    myIdf = myTfidf.idf()
    # print(myIdf)

    myTfIdfDict = myTfidf.tfidf(myTf, myIdf)
    sortedTfIdf = myTfidf.sortAndSelectByValue(myTfIdfDict)
    print("sortedDict ", sortedTfIdf)

    myTfidf.writeResult(sortedTfIdf, "results/result")
    #print(myTfIdfDict)
