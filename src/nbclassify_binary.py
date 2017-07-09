from collections import defaultdict
from collections import Counter
import math
import re
import sys

def getData(filename):
    fp = open(filename)
    lines = fp.readlines()
    return lines


def getTokens(line):
    tokens = re.findall('[a-zA-Z0-9\']+', line)
    return tokens


def createValidationTerms(review):
    terms = set()
    # for review in reviews:
    words = getTokens(review)
    identifier=words[0]
    for word in words[1:]:
        terms.add(word.lower().strip())
    #print(len(terms))
    return (identifier,terms)

def read_modeldata():
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    model_data=getData("nbmodel.txt")
    prior_dataset=model_data[0:4]
    prior_prob=dict()
    for prior_data in prior_dataset:
        tokens = re.findall('[a-zA-Z0-9\.]+', prior_data)
        prior_prob[tokens[0]]=float(tokens[1])
    #print(prior_prob)

    like_dataset=model_data[4:]
    like_prob=defaultdict(Counter)
    for like_data in like_dataset:
        like_data=like_data.strip('\n')
        tokens=like_data.split(',')
        # tokens = re.findall('[a-zA-Z0-9\.\-]+', prior_data)
        for index in range(0,4):
            like_prob[tokens[0]][label_sequence[index]]=float(tokens[index+1])
    return (prior_prob,like_prob)
    # for key in like_prob:
    #     print(key,'\t',like_prob[key])

def posterior_probability(prior_prob,like_prob,labels,words):
    score = dict()
    for label in labels:
        val=prior_prob[label]
        score[label] = math.log(prior_prob[label],math.e)
        for word in words:
            word=word.lower()
            if(like_prob[word][label]!=0):
                score[label] += math.log(like_prob[word][label],math.e)
    return score

def max_prob(score):
    list=sorted(score, key=score.__getitem__)
    return list[1]

def write_result(result):
    fp=open("nboutput.txt",mode='w')
    for line in result:
        fp.write(line)
        fp.write('\n')

def maximum_likelihood(prior_prob,like_prob,reviews):
    label_sequence1 = ['truthful', 'deceptive']
    label_sequence2 =['positive', 'negative']
    result=list()
    for review in reviews:
        # (identifier, words)=createValidationTerms(review)
        tokens=review.split()
        identifier = tokens[0]
        words=tokens[1:]
        score1=posterior_probability(prior_prob, like_prob, label_sequence1, words)
        score2=posterior_probability(prior_prob, like_prob, label_sequence2, words)
        print(score1)
        print(score2)
        result_line=identifier+" "+max_prob(score1)+" "+max_prob(score2)
        result.append(result_line)
        write_result(result)
        #print(result)
        # result_line=list()
        # result_line[0]=identifier
        # result_line[1]=max(score1,key=score1.__getitem__)
        # result_line[2]=max(score2, key=score2.__getitem__)



test_data = getData(sys.argv[1])
(prior_prob,like_prob)=read_modeldata()
maximum_likelihood(prior_prob,like_prob,test_data)
