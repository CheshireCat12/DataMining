import numpy as np
from random import randint
from tfidf import getListWordsFromFile
from ast import literal_eval


def kmeans(k, epsilon, X):
    N = len(X)
    size = len(X[0])
    #print(size)
    V = initV_vector(N-1, k, X)
    U = np.zeros(shape=(N, k))

    while True:
        for i in range(0, N):
            c = 0
            U[i][0] = 1

            for j in range(1, k):
                # print("j ", j, " c ", c)
                # print("X[i]: ", X[i])
                # print("V[c]: ", V[c])
                # print("V[j]: ", V[j])
                # print("dist(x[i], V[c]: ", euclideanDistance(X[i], V[c]))
                # print("dist(x[i], V[j]: ", euclideanDistance(X[i], V[j]))
                # print("---------")
                if euclideanDistance(X[i], V[c]) < euclideanDistance(X[i], V[j]):
                    U[i][j] = 0
                else:
                    U[i][j] = 1
                    U[i][c] = 0
                    c = j
            # print(U)
            # print("V ", V)
        #print(U)
        #print("V ", V)

        V1 = initV_vector(0, k, X)
        for c in range(k):
            vect1 = [0 for i in range(size)]
            somme1 = 0
            sommeEuclideanDist = 0
            for i in range(N):
                vecteurTemp = [U[i][c] * num for num in X[i]]
                vect1 = addVector(vect1, vecteurTemp)

            for i in range(N):
                somme1 += U[i][c]

            V1[c] = divideVectorByValue(vect1, somme1)

        # print(V1)

        for i in range(k):
            sommeEuclideanDist += euclideanDistance(V[i], V1[i])

        #print("euclidean dist ", sommeEuclideanDist)
        if sommeEuclideanDist < epsilon:
            break
        else:
            V = V1

    return (U, V)


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


def cosSinSimilarity(x, y):
    return myDot(x, y) / (myNorm(x) * myNorm(y))


def myDot(x, y):
    return sum([num1 * num2 for (num1, num2) in zip(x, y)])


def myNorm(x):
    poweredBy2 = [np.power(number, 2) for number in x]
    sumOfPower2 = sum(poweredBy2)
    return np.sqrt(sumOfPower2)


def loadListFromString(fileName):
    newListOfWord = []
    oldListOfWord = getListWordsFromFile(fileName)

    for word in oldListOfWord:
        newListOfWord.append(literal_eval(word))

    return np.array(newListOfWord)


if __name__ == "__main__":
    k = 10

    x = np.array([[0, 0, 0],
                  [7.9149087, 6.55160469, 4.23423],
                  [8.6754, 7.05160469, 3.1415],
                  [34.8127404, 20.67128041, 24.75654],
                  [2.04621601, 0.07401111, 2.56563],
                  [1.043211, 3.07486311, 1.73423],
                  [0.9453461, 0.574054671, 2.56563],
                  [32.04621601, 20.07401111, 25.56563]])

    #print(kmeans(k, 0.0004, x)[0])

    M = loadListFromString("results/resultArray.txt")

    print(kmeans(k, 0.0004, M)[0])

