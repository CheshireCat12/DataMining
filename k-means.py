import numpy as np
from random import randint
from tfidf import getListWordsFromFile, time_decorator
from ast import literal_eval
from copy import deepcopy


@time_decorator
def kmeans(k, epsilon, X):
    N = len(X)
    size = len(X[0])
    V = initV_vector(N - 1, k, X)
    variationJ = deepcopy(V)
    U = np.zeros(shape=(N, k))
    C = 1
    W = np.array([[C for i in range(size)] for j in range(k)])

    while True:
        for i in range(0, N):
            c = 0
            U[i][0] = 1

            for j in range(1, k):
                if d(X[i], V[c], W[j]) < d(X[i], V[j], W[j]):
                    U[i][j] = 0
                else:   
                    U[i][j] = 1
                    U[i][c] = 0
                    c = j

        V1 = initV_vector(0, k, X)
        for c in range(k):
            vect1 = [0 for i in range(size)]
            for i in range(N):
                vecteurTemp = [U[i][c] * num for num in X[i]]
                vect1 = addVector(vect1, vecteurTemp)

            somme1 = sum([U[i][c] for i in range(N)])

            V1[c] = divideVectorByValue(vect1, somme1)
            variationJ[c] = varianceVector(V[c], V1[c])

        W = np.array(computeNewWeight(W, C, variationJ))
        sommeEuclideanDist = sum([d(V[i], V1[i], W[i]) for i in range(k)])

        if sommeEuclideanDist < epsilon:
            break
        else:
            V = V1

    return (U, V)


def varianceVector(vect1, vect2):
    return [abs(num1 - num2) for num1, num2 in zip(vect1, vect2)]


def addVector(vect1, vect2):
    return [num1 + num2 for (num1, num2) in zip(vect1, vect2)]


def divideVectorByValue(vector, value):
    value = 1 if value == 0 else value
    return [num / value for num in vector]


def initV_vector(rangeOfInitValue, k, X):
    return np.array([X[(randint(0, rangeOfInitValue))] for i in range(k)])


def distCos(x, y):
    return 1 - cosSinSimilarity(x, y)


def euclideanDistance(x, y):
    somme = sum([np.power(num1 - num2, 2) for (num1, num2) in zip(x, y)])
    return np.sqrt(somme)


def d(x, y, w):
    somme = [np.power(num1 - num2, 2) for (num1, num2) in zip(x, y)]
    balencedSum = sum([(num1 * num2) for (num1, num2) in zip(somme, w)])
    return np.sqrt(balencedSum)


def cosSinSimilarity(x, y):
    return myDot(x, y) / (myNorm(x) * myNorm(y))


def myDot(x, y):
    return sum([num1 * num2 for (num1, num2) in zip(x, y)])


def myNorm(x):
    poweredBy2 = [np.power(number, 2) for number in x]
    sumOfPower2 = sum(poweredBy2)
    return np.sqrt(sumOfPower2)


def computeNewWeight(weight, C, variance):
    height = range(len(weight))
    width = range(len(weight[0]))

    newWeight = [[weight[i][j] / (1 + variance[i][j]) for j in width] for i in height]
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
                  [1.043211, 3.07486311, 1.73423, 2.3453],
                  [0.9453461, 0.574054671, 2.56563, 1.324],
                  [32.04621601, 20.07401111, 25.56563, 28.5938]])

    #print(kmeans(k, 0.0004, x)[0])

    M = loadListFromString("results/resultArray2.txt")
    cluster = kmeans(k, 0.0001, M)[0]

    print([lines for lines in cluster if lines[2] == 1])

    with open("results/cluster.txt", 'w+') as fileOut:
        dataOut = [str(lines) + "\n" for lines in cluster]
        fileOut.writelines(dataOut)
