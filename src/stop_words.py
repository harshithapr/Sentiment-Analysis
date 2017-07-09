import re
from collections import defaultdict
from collections import Counter

def countFrequencyOfwordsinclass(review_data, label_data):
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    review_class = dict.fromkeys(label_sequence, 0)
    list1 = list();
    review_map1 = dict();
    review_map2 = dict();
    for label_line in label_data:
        tokens = getTokens(label_line)
        review_map1[tokens[0]] = tokens[1]
        review_map2[tokens[0]] = tokens[2]
    print(review_map1.values())

    review_map = defaultdict(Counter)
    word_frequency = dict.fromkeys(createVocabulary(review_data), 0)
    for review in review_data:
        words = getTokens(review)
        for word in words[1:]:
            word_frequency[word.lower()] += 1
            review_class[review_map1[words[0]]] += 1
            review_class[review_map2[words[0]]] += 1
            review_map[word.lower()][review_map1[words[0]]] += 1
            review_map[word.lower()][review_map2[words[0]]] += 1
    #print(review_map)
    #print(review_class)
    #print(word_frequency)
    sortedlist=sorted(word_frequency, key=word_frequency.__getitem__)
    fw=open("words_frequency1.txt",mode='w')
    for word in reversed(sortedlist):
        fw.write(word)
        fw.write(',')
        fw.write(str(word_frequency[word]))
        fw.write('\n')

    return review_class, review_map

def getData(filename):
    fp = open(filename)
    lines = fp.readlines()
    return lines


def getTokens(line):
    tokens = re.findall('[a-zA-Z0-9\']+', line)
    return tokens

def createVocabulary(reviews):
    vocab = set()
    for review in reviews:
        words = getTokens(review)
        for word in words[1:]:
            vocab.add(word.lower().strip())
    print(len(vocab))
    return vocab

review_data = getData("train-text.txt")
vocabset = createVocabulary(review_data)

label_data = getData("train-labels.txt")

(wordsinclass, wordcountinclass) = countFrequencyOfwordsinclass(review_data, label_data)