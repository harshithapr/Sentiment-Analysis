from collections import Counter
from collections import defaultdict
import re
import sys

def get_labels():
    label_sequence1 = ['truthful', 'deceptive']
    label_sequence2 = ['positive', 'negative']
    labels_dict=dict()
    count=1;
    for label1 in label_sequence1:
        labels_dict[label1]=dict()
        for label2 in label_sequence2:
            labels_dict[label1][label2]=count
            count += 1
    return labels_dict;

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
                    # if word.lower() not in stop_words:
                vocab.add(word.lower().strip())
    # print(len(vocab))
    return vocab


def count_docs_in_Class(label_data):
    # label_sequence = get_labels()
    labels=get_labels()
    count = {1:0,2:0,3:0,4:0}
    for line in label_data:
        tokens = get_tokens(line)
        key_label=labels[tokens[1]][tokens[2]]
        count[key_label] += 1
    print("No of docs in class: ",count)
    return count


def count_frequency_of_words_in_class(review_data, label_data):
    labels = get_labels()
    list1 = list();
    label_map = dict();
    # review_map2 = dict();
    for label_line in label_data:
        tokens = get_tokens(label_line)
        label_map[tokens[0]] = labels[tokens[1].lower()][tokens[2].lower()]
        # review_map2[tokens[0]] = tokens[2].lower()
    print(label_map)
    # print(review_map2)

    review_map = defaultdict(Counter)
    # word_frequency = dict.fromkeys(create_vocabulary(review_data), 0)
    review_class = {1:0,2:0,3:0,4:0}
    # for label_id in [1,2,3,4]:
    #     review_map[label_id]=dict()
    for review in review_data:
        words=get_tokens(review)
        identifier=words[0]
        for word in words[1:]:
            # word_frequency[word.lower()] += 1
            review_class[label_map[identifier]] += 1
            review_map[label_map[identifier]][word.lower()] += 1
            # review_map[word.lower()][review_map2[identifier]] += 1

    print(review_class)
    print(review_map)
    # print(word_frequency)

    # sortedlist=sorted(word_frequency, key=word_frequency.__getitem__)
    # fw=open("words_frequency2.txt",mode='w')
    # for word in reversed(sortedlist):
    #     fw.write(word)
    #     fw.write(',')
    #     fw.write(str(word_frequency[word]))
    #     fw.write('\n')

    return review_class, review_map


def calculatePriorProbability(priorclassfrequency, numberofdocs):
    labels=[1,2,3,4]
    priorclassprobability = dict()
    for label in labels:
        priorclassprobability[label] = priorclassfrequency[label] / numberofdocs
    print(priorclassprobability)
    return priorclassprobability


def calculateLikelihood(vocab, wordsinclass, wordcountinclass):
    labels=[1,2,3,4]
    likelihoodProbability = defaultdict(Counter)
    for label in labels:
        for word in vocab:
            likelihoodProbability[label][word] = (wordcountinclass[label][word] + 1) / (wordsinclass[label] + len(vocab))
    print(likelihoodProbability)
    return likelihoodProbability


def writeModel(prior, likelihood, vocab):
    labels = [1,2,3,4]
    fp = open("nbmodel.txt", mode='w')
    for label in labels:
        fp.write(str(label) + ',' + str(prior[label]))
        fp.write("\n")

    for word in vocab:
        fp.write(word)
        for label in labels:
            fp.write(',' + str(likelihood[label][word]))
        fp.write("\n")


review_data = get_data(sys.argv[1])
vocabset = create_vocabulary(review_data)
print(len(vocabset))

label_data = get_data(sys.argv[2])
priorclassfrequency = count_docs_in_Class(label_data)
#print(priorclassfrequency)

(wordsinclass, wordcountinclass) = count_frequency_of_words_in_class(review_data, label_data)
prior = calculatePriorProbability(priorclassfrequency, len(review_data))
likelihood = calculateLikelihood(vocabset, wordsinclass, wordcountinclass)
writeModel(prior, likelihood, vocabset)
