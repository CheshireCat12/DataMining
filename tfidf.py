from math import log
from copy import deepcopy
import time
import operator
from functools import wraps


class Tfidf:

    def __init__(self, document, numberOfWordChosen):
        print("Creation of the class...")
        self.numberOfWordPerDocument = {}
        self.frequencePerWordInDocument = {}
        self.nbOccurenceWordInDocument = {}
        self.document = document
        self.numberOfWordChosen = numberOfWordChosen

    def name_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("The function {0} is executed...\n".format(func.__name__))
            result = func(*args, **kwargs)
            return result
        return wrapper

    @name_decorator
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

    @name_decorator
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

    @name_decorator
    def idf(self):
        numberOfDocument = self.getNumberOfDocument()
        copyOfOccurenceWord = deepcopy(self.nbOccurenceWordInDocument)

        for termId in copyOfOccurenceWord:
            copyOfOccurenceWord[termId] = log(
                numberOfDocument / copyOfOccurenceWord[termId])

        return copyOfOccurenceWord

    @name_decorator
    def tfidf(self, tfDict, idfDict):
        tfidfPerWords = {}

        for doc in tfDict:
            for words in tfDict[doc]:
                self.getNumberOfOccurence(
                    words, tfDict[doc][words], tfidfPerWords)

        for words in tfidfPerWords:
            tfidfPerWords[words] *= idfDict[words]

        return tfidfPerWords

    @name_decorator
    def sortAndSelectByValue(self, dictionary):
        sortedDictionary = sorted(
            dictionary.items(), key=operator.itemgetter(1), reverse=True)

        return sortedDictionary[:self.numberOfWordChosen]

    @name_decorator
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

        with open(fileNameOut + "Array.txt", 'w+') as fileOut:
            for lines in result:
                fileOut.writelines(str(result[lines]) + "\n")

    def writeResultWords(self, selectedWord, fileNameOut):
        arrayOut = [k + " " + str(v) + "\n" for k, v in selectedWord]
        with open(fileNameOut + "Words.txt", "w+") as fileOut:
            fileOut.writelines(arrayOut)


def time_decorator(func):
    def wrapper(*args, **kwargs):
        print("The function {0} is executed...".format(func.__name__))
        start = time.clock()
        result = func(*args, **kwargs)
        end = time.clock()
        print('{0} is executed in {1}s'.format(func.__name__, end-start))
        return result
    return wrapper


@time_decorator
def loadAllData(fileName):
    dataLoaded = list()

    for i in range(1, 4):
        data = getListWordsFromFile(fileName.format(i))
        dataLoaded += data

    return dataLoaded


def getListWordsFromFile(fileName):
    with open(fileName) as fileIn:
        return fileIn.readlines()


@time_decorator
def main():
    fileName = "nsfabs_part{0}_out/docwords.txt"
    docWords = loadAllData(fileName)

    myTfidf = Tfidf(docWords, 5)
    myTfidf.getNumberOfWordInEachDocument()

    myTf = myTfidf.tf()
    myIdf = myTfidf.idf()

    myTfIdfDict = myTfidf.tfidf(myTf, myIdf)
    sortedTfIdf = myTfidf.sortAndSelectByValue(myTfIdfDict)

    myTfidf.writeResult(sortedTfIdf, "results/result")


if __name__ == "__main__":
    main()
