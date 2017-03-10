from collections import Counter
from collections import defaultdict
import re


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


def countDocsInClass(label_data):
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    count = dict.fromkeys(label_sequence, 0)
    for line in label_data:
        tokens = getTokens(line)
        count[tokens[1].lower()] += 1
        count[tokens[2].lower()] += 1
    return count


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
    print(review_map)
    print(review_class)
    print(word_frequency)
    print(sorted(word_frequency, key=word_frequency.__getitem__))
    return review_class, review_map


def calculatePriorProbability(priorclassfrequency, numberofdocs):
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    priorclassprobability = dict.fromkeys(label_sequence, 0)
    for key in priorclassfrequency:
        priorclassprobability[key] = priorclassfrequency[key] / numberofdocs
    # print(priorclassprobability)
    return priorclassprobability


def calculateLikelihood(vocab, wordsinclass, wordcountinclass):
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    likelihoodProbability = defaultdict(Counter)
    for label in label_sequence:
        for key in vocab:
            likelihoodProbability[key][label] = (wordcountinclass[key][label] + 1) / (wordsinclass[label] + len(vocab))
    # print(likelihoodProbability)
    return likelihoodProbability


def writeModel(prior, likelihood, vocab):
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    fp = open("nbmodel.txt", mode='w')
    for key in prior:
        fp.write(key + ',' + str(prior[key]))
        fp.write("\n")

    for word in vocab:
        fp.write(word)
        for label in label_sequence:
            fp.write(',' + str(likelihood[word][label]))
        fp.write("\n")


review_data = getData("train-text.txt")
vocabset = createVocabulary(review_data)

label_data = getData("train-labels.txt")
priorclassfrequency = countDocsInClass(label_data)
print(priorclassfrequency)
(wordsinclass, wordcountinclass) = countFrequencyOfwordsinclass(review_data, label_data)
prior = calculatePriorProbability(priorclassfrequency, len(review_data))
likelihood = calculateLikelihood(vocabset, wordsinclass, wordcountinclass)
writeModel(prior, likelihood, vocabset)
