# -*- coding: utf-8 -*-
"""classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t4xh9A7QawcY0kjoH1HP7Gkmm1caO_6R
"""

# from google.colab import drive
# drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My\ Drive/Colab\ Notebooks/Hi_Im_Bot

# !pwd

# !pip install tensorflow==1.14
# !pip install numpy
# !pip install tflearn

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

nltk.download('punkt')

"""**Loading the pickle created in the previous notebook**"""

import pickle
data = pickle.load( open("training_data", "rb" ) )
print(data)

words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

import json
with open('intents.json',encoding='utf-8') as json_data:
    intents = json.load(json_data)

#print(intents)

net = tflearn.input_data(shape=[None, len(train_x[0])])
hidden_layers = 2
for i in range(hidden_layers):
  net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
# net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net,  tensorboard_verbose=0, tensorboard_dir='tflearn_logs')

"""**Visualization Using TensorBoard**"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# !rm -rf ./logs/ #to delete previous runs
# # %tensorboard --logdir logs/
# !pip uninstall tensorboard-plugin-wit
# !tensorboard --logdir='/content/drive/My Drive/Colab Notebooks/Hi_Im_Bot/tflearn_logs/20QYS9'

"""**Preprocessing the given input**

The message/query given by the user is stemmed and converted into bag of words.
"""

def preprocess_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)

    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bag_of_words(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = preprocess_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

# load our saved model
model.load('model.tflearn')

#from IPython.display import Javascript

"""**Classification**

Rather than selecting a response in a random manner, we implement another filtering function called classify. This method calculates the probabilities of all the responses and filters all the responses whose score is less than the specified threshhold.

Note: The threshold can be adjusted according to the dataset and model architecture.
"""
import webbrowser


def open_web():
    webbrowser.open('https://transport.karnataka.gov.in/english')
#   url = 'https://www.google.com/'
#   display(Javascript('window.open("{url}");'.format(url=url)))


context = {}

threshold = 0.70
def classify(sentence):
    # calculating probabilities from the model
    results = model.predict([bag_of_words(sentence, words)])[0]
    #print("class results:",results)

    # filtering out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>threshold]
    #print("resutls:",results)

    # sorting by probability in descending order
    results.sort(key=lambda x: x[1], reverse=True)
    final_list = []

    for r in results:
        final_list.append((classes[r[0]], r[1]))

    # return tuple of intent and probability
    return final_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)

    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # a random response from the intent
                    return random.choice(i['responses'])

            results.pop(0)
    else:
      open_web()
      return "I dont understand, please google it"

"""**Finally it is time to chat with the BOT**"""

def chat_with_bot(query):
    print("class input:",query)
    return response(query)
      #query = input()

#!pip install import-ipynb

#print("Start chatting with me. Press quit if you are bored \n")
#first_msg = input()
#chat_with_bot(first_msg)
#exec(open('gui.py').read())