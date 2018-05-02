#==============import packages
import keras.backend.tensorflow_backend
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re

#==============get data
#data = pd.read_csv('Final_datasets/Dataset_1.csv', encoding="latin1")
#data = pd.read_csv('Final_datasets/Dataset_2.csv', encoding="latin1")
#data = pd.read_csv('Final_datasets/Dataset_3.csv', encoding="latin1")
#data = pd.read_csv('Final_datasets/Dataset_4.csv', encoding="latin1")
#data = pd.read_csv('Final_datasets/Dataset_5.csv', encoding="latin1")
data = pd.read_csv('Final_datasets/Dataset_6.csv', encoding="latin1")
data.head(5)
#0 is sentiment negative
#1 is sentiment positive

print("negative:")
print(data[ data['Sentiment'] == 0].size)
print("positive:")
print(data[ data['Sentiment'] == 1].size)
print("neutral:")
print(data[ data['Sentiment'] == 2].size)

#==============data transformation
data['SentimentText'] = data['SentimentText'].apply(lambda x: x.lower())
data['SentimentText'] = data['SentimentText'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))

#==============input for the model
max_fatures = 2000
tokenizer = Tokenizer(num_words=max_fatures, split=' ')  #an object of class. max words kept=2000
tokenizer.fit_on_texts(data['SentimentText'].values)     #for every word in the texts, a frequency is calculated n stored
#print(tokenizer.word_index)                             #print the words fit by the tokenizer
X = tokenizer.texts_to_sequences(data['SentimentText'].values)  #returns a list of integers; one integer for one word; the integer value represents the frequency of that word in the text
X = pad_sequences(X)                                     #make all the lengths equal; so that they can be passed to the model

"""
    #=============== Model specification (Word2Vec)
    embeddings = {}
    glove_vec = 'Glove/glove.6B.50d.txt'
    f = open(glove_data)
    for line in f:
        values = line.split()
        word = values[0]
        value = np.asarray(values[1:], dtype='float32')
        embeddings[word] = value
    f.close()
    embed_dim = 10
    word_index = tokenizer.word_index
    embed_matrix = np.zeros((len(word_index) + 1, embed_dim))
    for word, i in word_index.items():
        embed_vec = embeddings.get(word)
        if embed_vector is not None:
            embed_matrix[i] = embed_vector[:embed_dim]
    embedding_layer = Embedding(embed_matrix.shape[0], embed_matrix.shape[1], weights=[embedding_matrix], input_length=12)
    
    model = Sequential()
    model.add(embedding_layer)                                      #embedding layer = word2vec
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))     #number of nodes=196
    model.add(Dense(3,activation='softmax'))                        #softmax layer with 3 node outputs
    model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
    print(model.summary())
"""

#==============Model specification (keras Embedding layer)
embed_dim = 128
lstm_out = 196

model = Sequential()
model.add(Embedding(max_fatures, embed_dim,input_length = X.shape[1])) #creates a vector space of dimension lstm_out; for every word in max_features words, it returns the location of the word in vector space.
model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))     #number of nodes=196
model.add(Dense(3,activation='softmax'))                        #softmax layer with 3 node outputs
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())

#==============separate train & test data, and save
Y = pd.get_dummies(data['Sentiment']).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.33, random_state = 42)
print("train shape:")
print(X_train.shape,Y_train.shape)
print("test shape:")
print(X_test.shape,Y_test.shape)

np.save('val_test/xtest',X_test)
np.save('val_test/ytest',Y_test)

#==============train the model, and save
batch_size = 48
model.fit(X_train, Y_train, epochs = 7, batch_size=batch_size, verbose = 2)

filename = 'model_train1.sav'
model.save('saved_models/mymodel.h5')

