import tfidf


if __name__ == "__main__":
    words = tfidf.getListWordsFromFile("words.txt")
    occurenceWord = tfidf.getListWordsFromFile("results/resultWords.txt")

    for word in occurenceWord:
        print(words[int(word.split()[0])])
