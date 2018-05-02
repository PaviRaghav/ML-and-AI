from collections import Counter
import re
import csv
import numpy as np
from sklearn import metrics

with open("Final_datasets/Dataset_Bayes.csv", 'r') as file:
    data1 = list(csv.reader(file))
data1.pop(0)
#0 negative
#1 positive
#2 neutral

s = 30000
data = data1[:-s]
test = data1[-s:]

#print(test[:5])


def getText(data, y):
    return " ".join([a[1].lower() for a in data if a[0] == str(y)])

def countWords(data):
    words = re.split("\s+", data)
    return Counter(words)

def getNumOfClassification(y):
    return len([a for a in data if a[0] == str(y)])

def make_prediction(text, counts, class_prob, class_count):
    prediction = 1
    text_counts = Counter(re.split("\s+", text))
    for word in text_counts:
        prediction *=  text_counts.get(word) * ((counts.get(word, 0) + 1) / (sum(counts.values()) + class_count))
    #print(prediction)
    # Now we multiply by the probability of the class existing in the documents.
    #print("prediction: ")
    #print(prediction)
    #print("=================================")
    return prediction * class_prob

def predict_all(text, negative_counts, prob_negative, negative_review_count, positive_counts, prob_positive, positive_review_count, neutral_counts, prob_neutral, neutral_review_count):
    #predictions = [predict_all(r[1], negative_word_counts, prob_negative, negative_word_counts, positive_word_counts, prob_positive, positive_word_counts, neutral_word_counts, prob_neutral, neutral_word_counts) for r in test]
    
    #(data[21][1], negative_word_counts, prob_negative, negative_data_count)
    
    # Compute the negative and positive probabilities.
    negative_prediction = make_prediction(text, negative_counts, prob_negative, negative_review_count)
    positive_prediction = make_prediction(text, positive_counts, prob_positive, positive_review_count)
    neutral_prediction = make_prediction(text, neutral_counts, prob_neutral, neutral_review_count)
    
    # We assign a classification based on which probability is greater.
    if (negative_prediction > positive_prediction) and (negative_prediction > neutral_prediction):
        return 0
    elif(positive_prediction > neutral_prediction):
        return 1
    else:
        return 2

#print("data:")
#print(data[0][0])
#print(data[0][1])
#print(data[1][0])
#print(data[1][1])
#print(data[2][0])
#print(data[2][1])
#print("=================================")
negative_text = getText(data, 0)
positive_text = getText(data, 1)
neutral_text = getText(data, 2)

# Generate word counts for negative tone.
negative_word_counts = countWords(negative_text)
# Generate word counts for positive tone.
positive_word_counts = countWords(positive_text)
# Generate word counts for neutral tone.
neutral_word_counts = countWords(neutral_text)

#print("Negative text sample: {0}".format(negative_text[:150]))
#print("Positive text sample: {0}".format(positive_text[:150]))
#print("Neutral text sample: {0}".format(neutral_text[:150]))

positive_data_count = getNumOfClassification(1)
negative_data_count = getNumOfClassification(0)
neutral_data_count = getNumOfClassification(2)

prob_positive = positive_data_count / len(data)
prob_negative = negative_data_count / len(data)
prob_neutral = neutral_data_count / len(data)
#print("pos: {0}, neg: {1}, neut: {2}".format(prob_positive,prob_negative,prob_neutral))
#print("=================================")


"""
negative_word_counts, prob_negative, negative_word_counts, positive_word_counts, prob_positive, positive_word_counts, neutral_word_counts, prob_neutral, neutral_word_counts

print("Text: {0}, prediction: {1}".format(data[21][1], data[21][0]))
print("Negative prediction: {0}".format(make_prediction(data[21][1], negative_word_counts, prob_negative, negative_data_count)))
print("Positive prediction: {0}".format(make_prediction(data[21][1], positive_word_counts, prob_positive, positive_data_count)))
print("Neutral prediction: {0}".format(make_prediction(data[21][1], neutral_word_counts, prob_neutral, neutral_data_count)))
"""

predictions = [predict_all(r[1], negative_word_counts, prob_negative, negative_data_count, positive_word_counts, prob_positive, positive_data_count, neutral_word_counts, prob_neutral, neutral_data_count) for r in test]

actual = [int(r[0]) for r in test]
acc = metrics.accuracy_score(actual, predictions, normalize=True)

print("accuracy: {0}".format(acc))
