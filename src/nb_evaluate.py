from collections import defaultdict


def get_labels():
    label_sequence = ['truthful', 'deceptive', 'positive', 'negative']
    return label_sequence


def open_predicted_output():
    lines = [line.rstrip() for line in open("nboutput.txt")]
    return lines


def open_actual_output():
    lines = [line.rstrip() for line in open("dev-output.txt")]
    return lines


def get_number_of_predictions():
    return len(open_predicted_output())


def get_predicted_output():
    predictions = open_predicted_output()
    predicted_map = defaultdict()
    for label in get_labels():
        predicted_map[label] = list()
    for prediction in predictions:
        predicted_tokens = prediction.split(' ')
        predicted_map[predicted_tokens[1]].append(predicted_tokens[0])
        predicted_map[predicted_tokens[2]].append(predicted_tokens[0])
    return predicted_map


def get_actual_output():
    actuals = open_actual_output()
    actual_map = defaultdict()
    for label in get_labels():
        actual_map[label] = list()
    for actual in actuals:
        actual_tokens = actual.split(' ')
        if actual_tokens[1] == 'We':
            print(actual_tokens[1])
        actual_map[actual_tokens[1]].append(actual_tokens[0])
        actual_map[actual_tokens[2]].append(actual_tokens[0])
    return actual_map


def get_contingency_table():
    predicted_map = get_predicted_output()
    actual_map = get_actual_output()
    tp = dict.fromkeys(get_labels(), 0)
    fp = dict.fromkeys(get_labels(), 0)
    fn = dict.fromkeys(get_labels(), 0)
    tn = dict.fromkeys(get_labels(), 0)

    for label in get_labels():
        for actual in actual_map[label]:
            if actual in predicted_map[label]:
                tp[label] += 1
            else:
                fn[label] += 1
        for prediction in predicted_map[label]:
            if prediction not in actual_map[label]:
                fp[label] += 1
        tn[label] = get_number_of_predictions() - (tp[label] + fp[label] + fn[label])
    return (tp, fp, fn, tn)


def evaluation_metrics():
    (tp, fp, fn, tn) = get_contingency_table()
    precision_score = dict()
    recall_score = dict()
    f1_score = dict()
    for label in get_labels():
            precision_score[label] = tp[label] / (tp[label] + fp[label])
            recall_score[label] = tp[label] / (tp[label] + fn[label])
            f1_score[label] = (2 * precision_score[label] * recall_score[label]) / (precision_score[label] + recall_score[label])
    return (precision_score, recall_score, f1_score)

def weighted_average(predicted_map,f1_score):
    avg=0

    for label in get_labels():
        avg += f1_score[label]
    return avg/len(get_labels())

print(get_actual_output())
print(get_predicted_output())
(tp, fp, fn, tn) = get_contingency_table()
print(get_number_of_predictions())
for label in get_labels():
    print(label)
    print(tp[label],' ',fp[label])
    print(fn[label],' ',tn[label])

(P,R,F1)=evaluation_metrics()
# for label in get_labels():
#     print(label,' ',P[label],' ',R[label],' ',F1[label])

print(weighted_average(get_predicted_output(),F1))

