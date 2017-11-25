import numpy as np
from random import randint
from tfidf import getListWordsFromFile, time_decorator
from ast import literal_eval
from copy import deepcopy


@time_decorator
def hierarchique(k, X):
    N = len(X)

    matrix = np.zeros(shape=(N, N))
    for i in range(N):
        for j in range(N):
            if j < i:
                matrix[i][j] = euclideanDistance(X[i], X[j])

    minDistInMatrix = findMinDist(matrix, range(1, N))
    dendogram = cluster = findIndexMinDist(matrix, minDistInMatrix)

    print(matrix)
    newMatrix = cutMatrix(matrix, cluster[0])
    print(newMatrix)
    for j in range(len(newMatrix)):
        indexToChange = cluster[1][0]
        if newMatrix[indexToChange][j] != float(0):
            newMatrix[indexToChange][j] = minValue(cluster, j, X)

        if newMatrix[j][indexToChange] != 0:
            newMatrix[j][indexToChange] = minValue(cluster, j, X)

    print(newMatrix)
    return "temp"


def cutMatrix(matrix, index):
    mat = np.delete(matrix, index, 0)
    mat2 = np.delete(mat, index, 1)

    return mat2


def updateMatrix(matrix, cluster):
    matrixLen = len(matrix) - 1
    for i in range(matrixLen):
        for j in range(matrixLen):
            if j < i:
                pass


def minValue(cluster, index, X):
    distance1 = euclideanDistance(X[cluster[1][0]], X[index])
    distance2 = euclideanDistance(X[cluster[0][0]], X[index])
    return min(distance1, distance2)


def findIndexMinDist(matrix, minDistInMatrix):
    index = np.where(matrix == minDistInMatrix)
    indexI = index[0]
    indexJ = index[1]
    return (indexI, indexJ)


def findMinDist(matrix, rangeMatrix):
    minimumInMatrix = [min([i for i in matrix[j] if i > 0.])
                       for j in rangeMatrix]

    minimumInMatrix = min(minimumInMatrix)
    return minimumInMatrix


def addVector(vect1, vect2):
    return [num1 + num2 for (num1, num2) in zip(vect1, vect2)]


def initV_vector(rangeOfInitValue, k, X):
    return np.array([X[(randint(0, rangeOfInitValue))] for i in range(k)])


def euclideanDistance(x, y):
    somme = sum([np.power(num1 - num2, 2) for (num1, num2) in zip(x, y)])
    return np.sqrt(somme)


def computeNewWeight(weight, C, variance):
    height = range(len(weight))
    width = range(len(weight[0]))

    newWeight = [[weight[i][j] / (1 + variance[i][j])
                  for j in width] for i in height]
    normalizedWeight = [
        [C * newWeight[i][j] / computeSquaredWeight(newWeight[i]) for j in width] for i in height]

    return normalizedWeight


def computeSquaredWeight(weightK):
    sumWeight = sum([np.power(weightKI, 2) for weightKI in weightK])
    squaredSum = np.sqrt(sumWeight)
    return squaredSum


@time_decorator
def loadListFromString(fileName):
    newListOfWord = []
    oldListOfWord = getListWordsFromFile(fileName)

    newListOfWord = [literal_eval(word) for word in oldListOfWord]
    return np.array(newListOfWord)


if __name__ == "__main__":
    k = 6

    x = np.array([[0, 0, 0, 0],
                  [7.9149087, 6.55160469, 4.23423, 5.6754],
                  [8.6754, 7.05160469, 3.1415, 6.09847],
                  [34.8127404, 20.67128041, 24.75654, 26.59382],
                  [2.04621601, 0.07401111, 2.56563, 1.2321],
                  [1.043211, 3.07486311, 1.73423, 2.3453]])
    #[0.9453461, 0.574054671, 2.56563, 1.324],
    #[32.04621601, 20.07401111, 25.56563, 28.5938]])

    #print(hierarchique(k, 0.0004, x)[0])

    #M = loadListFromString("results/resultArray2.txt")
    cluster = hierarchique(k, x)[0]

    # with open("results/cluster.txt", 'w+') as fileOut:
    #     dataOut = [str(lines) + "\n" for lines in cluster]
    # fileOut.writelines(dataOut)
