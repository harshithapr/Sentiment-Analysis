from collections import Counter
from collections import defaultdict
import re

def get_labels():
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    return label_sequence

def get_data(filename):
    fp = open(filename)
    lines = fp.readlines()
    return lines

def read_stop_words():
    stop_words_list=[line.rstrip() for line in open("stop_words.txt")]
    return stop_words_list


def get_tokens(line):
    tokens = re.findall('[a-zA-Z0-9\']+', line)
    return tokens


def create_vocabulary(reviews):
    vocab = set()
    stop_words=read_stop_words()
    for review in reviews:
        words = get_tokens(review)
        for word in words[1:]:
            if not (word.isdigit()):
                    if word.lower() not in stop_words:
                        vocab.add(word.lower().strip())
    # print(len(vocab))
    return vocab


def count_docs_in_Class(label_data):
    label_sequence = get_labels()
    count = dict.fromkeys(label_sequence, 0)
    for line in label_data:
        tokens = get_tokens(line)
        count[tokens[1].lower()] += 1
        count[tokens[2].lower()] += 1
    return count


def count_frequency_of_words_in_class(review_data, label_data):
    label_sequence = get_labels()
    review_class = dict.fromkeys(label_sequence, 0)
    list1 = list();
    review_map1 = dict();
    review_map2 = dict();
    for label_line in label_data:
        tokens = get_tokens(label_line)
        review_map1[tokens[0]] = tokens[1]
        review_map2[tokens[0]] = tokens[2]
    print(review_map1.values())

    review_map = defaultdict(Counter)
    word_frequency = dict.fromkeys(create_vocabulary(review_data), 0)
    for review in review_data:
        identifier = review.split()[0]
        review_list = list()
        review_list.append(review)
        words_set = create_vocabulary(review_list)
        words = list()
        for word in words_set:
            words.append(word)
        for word in words:
            word_frequency[word.lower()] += 1
            review_class[review_map1[identifier]] += 1
            review_class[review_map2[identifier]] += 1
            review_map[word.lower()][review_map1[identifier]] += 1
            review_map[word.lower()][review_map2[identifier]] += 1
    print(review_map)
    print(review_class)
    print(word_frequency)

    sortedlist=sorted(word_frequency, key=word_frequency.__getitem__)
    fw=open("words_frequency2.txt",mode='w')
    for word in reversed(sortedlist):
        fw.write(word)
        fw.write(',')
        fw.write(str(word_frequency[word]))
        fw.write('\n')

    return review_class, review_map


def calculatePriorProbability(priorclassfrequency, numberofdocs):
    label_sequence = get_labels()
    priorclassprobability = dict.fromkeys(label_sequence, 0)
    for key in priorclassfrequency:
        priorclassprobability[key] = priorclassfrequency[key] / numberofdocs
    # print(priorclassprobability)
    return priorclassprobability


def calculateLikelihood(vocab, wordsinclass, wordcountinclass):
    label_sequence = get_labels()
    likelihoodProbability = defaultdict(Counter)
    for label in label_sequence:
        for key in vocab:
            likelihoodProbability[key][label] = (wordcountinclass[key][label] + 1) / (wordsinclass[label] + len(vocab))
    # print(likelihoodProbability)
    return likelihoodProbability


def writeModel(prior, likelihood, vocab):
    label_sequence = get_labels()
    fp = open("nbmodel.txt", mode='w')
    for key in prior:
        fp.write(key + ',' + str(prior[key]))
        fp.write("\n")

    for word in vocab:
        fp.write(word)
        for label in label_sequence:
            fp.write(',' + str(likelihood[word][label]))
        fp.write("\n")


review_data = get_data("train-text.txt")
vocabset = create_vocabulary(review_data)
print(len(vocabset))

label_data = get_data("train-labels.txt")
priorclassfrequency = count_docs_in_Class(label_data)
print(priorclassfrequency)
(wordsinclass, wordcountinclass) = count_frequency_of_words_in_class(review_data, label_data)
prior = calculatePriorProbability(priorclassfrequency, len(review_data))
likelihood = calculateLikelihood(vocabset, wordsinclass, wordcountinclass)
writeModel(prior, likelihood, vocabset)
